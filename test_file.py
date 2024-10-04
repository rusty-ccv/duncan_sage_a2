
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#class Attribute getters and setters used genAI to copy from hand written code
#logging used genAI to copy from hand written print() code
class Location:
    def __init__(self, location_name):
        self.location_name = location_name

    # private getters and setters
    @property
    def location_name(self):
        return self._location_name
    
    @location_name.setter
    def location_name(self, location_name):
        if not isinstance(location_name, str):
            raise ValueError("location_name must be a string")
        self._location_name = location_name

class Forecast(Location):
    def __init__(self, location_name, upload_date, forecast_date, min_temp, max_temp,
                 condition, rainfall_possible, rainfall_chance, forecast, warning):
        super().__init__(location_name)
        self.upload_date = upload_date
        self.forecast_date = forecast_date
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.condition = condition
        self.rainfall_possible = rainfall_possible
        self.rainfall_chance = rainfall_chance
        self.forecast = forecast
        self.warning = warning
    
    def print_contents(self):
        return (self.location_name, self.upload_date, self.forecast_date, self.min_temp, self.max_temp,
                self.condition, self.rainfall_possible, self.rainfall_chance, self.forecast, self.warning)
        
class DailyForecast(Forecast):
    pass

class WeeklyForecast:
    def __init__(self, upload_date):
        self.upload_date = upload_date
        self.daily_forecasts = {}

    def location_print(self, location_name):
        for daily_forecast in self.daily_forecasts.values():
            if daily_forecast.location_name == location_name:
                print(daily_forecast.print_contents())

    def print_contents(self):
        for daily_forecast in self.daily_forecasts.values():
            print(daily_forecast.print_contents())
    
    def add_daily_forecast(self, daily_forecast):
        if not isinstance(daily_forecast, DailyForecast):
            raise TypeError("daily_forecast must be an instance of DailyForecast")
        key = (daily_forecast.location_name, daily_forecast.forecast_date)
        if key not in self.daily_forecasts:
            self.daily_forecasts[key] = daily_forecast
            logging.info(f"Added DailyForecast to WeeklyForecast for upload date: {self.upload_date}")

class PageReader:
    def __init__(self, main):
        self.main = main
        self.links_list = []  # Initialize as a list
    
    # Get the subpages from the main page - created with the help of GenAI.
    def get_subpages(self, page_url):
        try:
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = [a['href'] for a in soup.find_all('a', href=True)]
            if links:
                self.links_list.extend(links[1:])  # Drop the first link and add the rest to the instance attribute list
            else:
                logging.error("No links found on the page.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error scraping page: {e}")
            return
        
        # Get data from website and create the objects - created with the help of GenAI.
    def scrape_page(self, page_url):
        for link in self.links_list:
            response = requests.get(page_url + "/" + link)
            soup = BeautifulSoup(response.content, 'html.parser')

            for div in soup.find_all('div', class_='day'):
                location_name = soup.find('title').text.split()[0]

                upload_date_str = soup.find('p', class_='date').text
                upload_date_str = upload_date_str.replace('EDT', '').strip().rstrip('.')  # Remove timezone abbreviation and trailing period
                upload_date = datetime.strptime(upload_date_str, 'Forecast updated at %I:%M %p on %A %d %B %Y')

                forecast_date_str = div.find('h2').text
                forecast_date = datetime.strptime(forecast_date_str, '%A %d %B')
                forecast_date = forecast_date.replace(year=upload_date.year)  # Set the year to the same as the upload date

                forecast_details = []
                list_items = div.find_all('li')
                for item in list_items:
                    forecast_details.append(item.text)

                min_temp = forecast_details[0]
                max_temp = forecast_details[1]
                condition = forecast_details[2]
                rainfall_possible = forecast_details[3]
                rainfall_chance = forecast_details[4]

                forecast = div.find('h3').text
                warning = div.find('p', class_='alert').text

                daily_forecast = DailyForecast(location_name, upload_date, forecast_date, min_temp, max_temp, condition, 
                                               rainfall_possible, rainfall_chance, forecast, warning)
                logging.info(f"Created DailyForecast: {location_name}, {forecast_date}")

                weekly_forecast = next((wf for wf in self.main.weekly_forecasts if wf.upload_date == upload_date), None)
                if not weekly_forecast:
                    weekly_forecast = WeeklyForecast(upload_date)
                    self.main.weekly_forecasts.append(weekly_forecast)
                    logging.info(f"Created new WeeklyForecast for upload date: {upload_date}")
                else:
                    logging.info(f"Found existing WeeklyForecast for upload date: {upload_date}")

                logging.info(f"Adding DailyForecast to WeeklyForecast for upload date: {upload_date}")
                weekly_forecast.add_daily_forecast(daily_forecast)

class Main:
    def __init__(self, page_url):
        self.page_url = page_url
        self.weekly_forecasts = []
        self.page_reader = PageReader(self)
        self.page_reader.get_subpages(page_url)
        self.page_reader.scrape_page(page_url)

    def print_contents(self):
        for weekly_forecast in self.weekly_forecasts:
            weekly_forecast.print_contents()

    def location_print(self, location_name):
        for weekly_forecast in self.weekly_forecasts:
            weekly_forecast.location_print(location_name)

class DataAnalysis:
    pass

######## test code ########
        
websiteURL = " https://prog2007.it.scu.edu.au/weather"
page1 = Main(websiteURL)


# # Print the forecast for Brisbane
location_name = "Melbourne"
page1.location_print(location_name)
# test scrape_page
#page1.page_reader.scrape_page(websiteURL)