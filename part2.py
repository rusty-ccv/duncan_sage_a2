﻿#Duncan Sage - 24034122






# Create a Python file called part2.py. Copy the code you wrote in part 1 into the part2.py file. Then update
# your code so that it:
# • Scrapes the data from the Sydney, Melbourne, and Brisbane pages using the request library and
# Beautiful Soup instead of reading it from a csv file.
# • Uses the datetime module for any date or time related data.
# • Uses the logging module to output appropriate messages where applicable e.g. info, warning, error
# messages.
# • Performs some basic data analysis using pandas instead of a set.
# You mark will be determined based on:
# • The criteria listed in the previous section.
# • How well you demonstrate the concepts you have learned in Module 5


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

    # protected getters and setters
    @property
    def upload_date(self):
        return self._upload_date
    
    @upload_date.setter
    def upload_date(self, upload_date):
        if not isinstance(upload_date, datetime):
            raise ValueError("upload_date must be a datetime object")
        self._upload_date = upload_date

    @property
    def forecast_date(self):
        return self._forecast_date
    
    @forecast_date.setter
    def forecast_date(self, forecast_date):
        if not isinstance(forecast_date, datetime):
            raise ValueError("forecast_date must be a datetime object")
        self._forecast_date = forecast_date
    
    @property
    def min_temp(self):
        return self._min_temp
    
    @min_temp.setter
    def min_temp(self, min_temp):
        if not isinstance(min_temp, str):
            raise ValueError("min_temp must be a string")
        self._min_temp = min_temp
    
    @property
    def max_temp(self):
        return self._max_temp
    
    @max_temp.setter
    def max_temp(self, max_temp):
        if not isinstance(max_temp, str):
            raise ValueError("max_temp must be a string")
        self._max_temp = max_temp

    @property
    def condition(self):
        return self._condition
    
    @condition.setter
    def condition(self, condition):
        if not isinstance(condition, str):
            raise ValueError("condition must be a string")
        self._condition = condition

    @property
    def rainfall_possible(self):
        return self._rainfall_possible

    @rainfall_possible.setter
    def rainfall_possible(self, rainfall_possible):
        if not isinstance(rainfall_possible, str):
            raise ValueError("rainfall_possible must be a string")
        self._rainfall_possible = rainfall_possible

    @property
    def rainfall_chance(self):
        return self._rainfall_chance
    
    @rainfall_chance.setter
    def rainfall_chance(self, rainfall_chance):
        if not isinstance(rainfall_chance, str):
            raise ValueError("rainfall_chance must be a string")
        self._rainfall_chance = rainfall_chance
    
    @property
    def forecast(self):
        return self._forecast
    
    @forecast.setter
    def forecast(self, forecast):
        if not isinstance(forecast, str):
            raise ValueError("forecast must be a string")
        self._forecast = forecast
    
    @property
    def warning(self):
        return self._warning
    
    @warning.setter
    def warning(self, warning):
        if not isinstance(warning, str):
            raise ValueError("warning must be a string")
        self._warning = warning
    
    def print_contents(self):
        return (self.location_name, self.upload_date, self.forecast_date, self.min_temp, self.max_temp,
                self.condition, self.rainfall_possible, self.rainfall_chance, self.forecast, self.warning)
        
class DailyForecast(Forecast):
    def to_dict(self):
        return {
            'location_name': self.location_name,
            'forecast_date': self.forecast_date,
            'min_temp': self.extract_number(self.min_temp),
            'max_temp': self.extract_number(self.max_temp),
            'condition': self.condition,
            'rainfall_possible_mm': self.extract_rainfall(self.rainfall_possible),
            'rainfall_chance_percent': self.extract_number(self.rainfall_chance)
        }

    # created with GenAI
    def extract_number(self, text):
        return float(''.join(filter(str.isdigit, text)))
    # created with GenAI
    def extract_rainfall(self, text):
        numbers = [float(num) for num in text.split() if num.replace('.', '', 1).isdigit()]
        return numbers if len(numbers) > 1 else numbers[0]

class WeeklyForecast:
    def __init__(self, upload_date):
        self.upload_date = upload_date
        self.daily_forecasts = {}

    @property
    def upload_date(self):
        return self._upload_date
    
    @upload_date.setter
    def upload_date(self, upload_date):
        if not isinstance(upload_date, datetime):
            raise ValueError("upload_date must be a datetime object")
        self._upload_date = upload_date

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

    @property
    def file_name(self):
        return self._file_name
    
    @file_name.setter
    def file_name(self, file_name):
        if not isinstance(file_name, str):
            raise ValueError("file_name must be a string")
        self._file_name = file_name

    def print_contents(self):
        for weekly_forecast in self.weekly_forecasts:
            weekly_forecast.print_contents()

    def location_print(self, location_name):
        for weekly_forecast in self.weekly_forecasts:
            weekly_forecast.location_print(location_name)

class DataAnalysis:
    def __init__(self, weekly_forecasts):
        self.weekly_forecasts = weekly_forecasts

    def forecasts_to_dataframe(self):
        data = []
        for weekly_forecast in self.weekly_forecasts:
            for daily_forecast in weekly_forecast.daily_forecasts.values():
                data.append(daily_forecast.to_dict())
        df = pd.DataFrame(data)
        return df
    def average_temperature_by_city(self):
        df = self.forecasts_to_dataframe()
        df['average_temp'] = (df['min_temp'] + df['max_temp']) / 2
        average_temp_by_city = df.groupby('location_name')['average_temp'].mean().reset_index()
        return average_temp_by_city
    
######## test code ########
        
websiteURL = " https://prog2007.it.scu.edu.au/weather"
page1 = Main(websiteURL)

# # Print the forecast for Brisbane
# location_name = "Melbourne"
# page1.location_print(location_name)

# data analysis
data_analysis = DataAnalysis(page1.weekly_forecasts)
average_temps = data_analysis.average_temperature_by_city()
print(average_temps)