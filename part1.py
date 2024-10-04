#Duncan Sage - 24034122

import csv

#class Attribute getters and setters used genAI to copy from hand written code
class Location:
    '''Location class to store the location name
    :param location_name: the name of the location ie. Brisbane    
    '''
    def __init__(self, location_name):
        self.location_name = location_name

    # private getters and setters
    @property
    def location_name(self):
        return self.__location_name
    
    @location_name.setter
    def location_name(self, location_name):
        if not isinstance(location_name, str):
            raise ValueError("location_name must be a string")
        self.__location_name = location_name

class Forecast(Location):
    '''Forecast class to store the forecast details. inherits from Location class and is the parent class of DailyForecast
    :param upload_date: the date the forecasts were uploaded
    :param forecast_date: the date of the forecast
    :param temperature_range: the range of temperatures for the forecast
    :param condition: the weather condition for the forecast
    :param rainfall_possible: the amount of rainfall possible (mm)
    :param rainfall_chance: the chance of rainfall (%)
    :param forecast: the forecast (text)
    :param warning: any UV warnings for the forecast
    '''
    def __init__(self, location_name, upload_date, forecast_date, temperature_range, 
                 condition, rainfall_possible, rainfall_chance, forecast, warning):
        super().__init__(location_name) # Call the parent class constructor
        self.upload_date = upload_date
        self.forecast_date = forecast_date
        self.temperature_range = temperature_range
        self.condition = condition
        self.rainfall_possible = rainfall_possible
        self.rainfall_chance = rainfall_chance
        self.forecast = forecast
        self.warning = warning

    # private getters and setters
    @property
    def upload_date(self):
        return self.__upload_date
    
    @upload_date.setter
    def upload_date(self, upload_date):
        if not isinstance(upload_date, str):
            raise ValueError("upload_date must be a string")
        self.__upload_date = upload_date

    @property
    def forecast_date(self):
        return self.__forecast_date
    
    @forecast_date.setter
    def forecast_date(self, forecast_date):
        if not isinstance(forecast_date, str):
            raise ValueError("forecast_date must be a string")
        self.__forecast_date = forecast_date
    
    @property
    def temperature_range(self):
        return self.__temperature_range
    
    @temperature_range.setter
    def temperature_range(self, temperature_range):
        if not isinstance(temperature_range, dict):
            raise ValueError("temperature_range must be a dictionary")
        self.__temperature_range = temperature_range

    @property
    def condition(self):
        return self.__condition
    
    @condition.setter
    def condition(self, condition):
        if not isinstance(condition, str):
            raise ValueError("condition must be a string")
        self.__condition = condition

    @property
    def rainfall_possible(self):
        return self.__rainfall_possible

    @rainfall_possible.setter
    def rainfall_possible(self, rainfall_possible):
        if not isinstance(rainfall_possible, str):
            raise ValueError("rainfall_possible must be a string")
        self.__rainfall_possible = rainfall_possible

    @property
    def rainfall_chance(self):
        return self.__rainfall_chance
    
    @rainfall_chance.setter
    def rainfall_chance(self, rainfall_chance):
        if not isinstance(rainfall_chance, str):
            raise ValueError("rainfall_chance must be a string")
        self.__rainfall_chance = rainfall_chance
    
    @property
    def forecast(self):
        return self.__forecast
    
    @forecast.setter
    def forecast(self, forecast):
        if not isinstance(forecast, str):
            raise ValueError("forecast must be a string")
        self.__forecast = forecast
    
    @property
    def warning(self):
        return self.__warning
    
    @warning.setter
    def warning(self, warning):
        if not isinstance(warning, str):
            raise ValueError("warning must be a string")
        self.__warning = warning
    
    def print_contents(self): 
        return (self.location_name, self.upload_date, self.forecast_date, self.temperature_range, self.temperature_range, 
                self.condition, self.rainfall_possible, self.rainfall_chance, self.forecast, self.warning)
        
class DailyForecast(Forecast):
    '''DailyForecast class to store the daily forecast details. Inherits from Forecast class'''
    pass

class WeeklyForecast:
    '''WeeklyForecast class to store the weekly forecast details. The date the forecasts were uploaded and the daily forecasts
    :param upload_date: the date the forecasts were uploaded
    :param daily_forecasts: the daily forecasts for the week in a dictionary
    '''
    def __init__(self, upload_date):
        self.upload_date = upload_date
        self.daily_forecasts = {}

    # private getters and setters
    @property
    def upload_date(self):
        return self.__upload_date
    
    @upload_date.setter
    def upload_date(self, upload_date):
        if not isinstance(upload_date, str):
            raise ValueError("upload_date must be a string")
        self.__upload_date = upload_date

    def print_contents(self):
        for daily_forecast in self.daily_forecasts.values():
            print(daily_forecast.print_contents())

    def location_print(self, location_name):
        for daily_forecast in self.daily_forecasts.values():
            if daily_forecast.location_name == location_name:
                print(daily_forecast.print_contents())
    
    def add_daily_forecast(self, daily_forecast):
        if not isinstance(daily_forecast, DailyForecast):
            raise TypeError("daily_forecast must be an instance of DailyForecast")
        key = (daily_forecast.location_name, daily_forecast.forecast_date)
        if key not in self.daily_forecasts:
            self.daily_forecasts[key] = daily_forecast
            print(f"Added forecast for {daily_forecast.location_name} on {daily_forecast.forecast_date}") # Debugging print statement

class CsvReader:
    '''CsvReader class to read the csv file and create the objects
    :param main: the main class object
    '''
    def __init__(self, main):
        self.main = main
    
    # read_csv method reads the csv file and creates the objects - created with the help of GenAI.
    def read_csv(self, file_name):
        try:
            with open(file_name, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header row if there is one
                for row in csv_reader:
                    temperature_range = self.temps_to_dict(row[3], row[4])
                    daily_forecast = DailyForecast(row[0], row[1], row[2], temperature_range, row[5], 
                                                   row[6], row[7], row[8], row[9])
                    weekly_forecast = next((wf for wf in self.main.weekly_forecasts if wf.upload_date == row[1]), None)
                    if not weekly_forecast:
                        weekly_forecast = WeeklyForecast(row[1])
                        self.main.weekly_forecasts.append(weekly_forecast)
                    weekly_forecast.add_daily_forecast(daily_forecast)
        except FileNotFoundError:
            print(f"Error: The file {file_name} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Convert temp_min and temp_max to floats and return them in a dictionary. GenAi used
    def temps_to_dict(self, temp_min_str, temp_max_str):
        try:
            temp_min_value = float(temp_min_str.split(': ')[1])
            temp_max_value = float(temp_max_str.split(': ')[1])
            return {'min': temp_min_value, 'max': temp_max_value}
        except (ValueError, IndexError) as e:
            print(f"Error converting temperatures: {e}")
            return {}

class Main:
    '''Main class to store the weekly forecasts and read the csv file
    :param file_name: the name of the csv file
    :param weekly_forecasts: the weekly forecasts in a list
    '''
    def __init__(self, file_name):
        self.file_name = file_name
        self.weekly_forecasts = []
        csv_reader = CsvReader(self)
        csv_reader.read_csv(self.file_name)

    # private getters and setters
    @property
    def file_name(self):
        return self.__file_name
    
    @file_name.setter
    def file_name(self, file_name):
        if not isinstance(file_name, str):
            raise ValueError("file_name must be a string")
        self.__file_name = file_name

    def print_contents(self):
        for weekly_forecast in self.weekly_forecasts:
            weekly_forecast.print_contents()

    def location_print(self, location_name):
        for weekly_forecast in self.weekly_forecasts:
            weekly_forecast.location_print(location_name)

class DataAnalysis:
    '''DataAnalysis class to analyse the data and find the average temperature
    :param main: the main class object
    :param average_temperature: the average temperature from the average_temperature method
    '''
    def __init__(self, main):
        self.main = main
        self.average_temperature = 0
    
    # private getters and setters
    @property
    def average_temperature(self):
        return self.__average_temperature
    
    @average_temperature.setter
    def average_temperature(self, average_temperature):
        if not isinstance(average_temperature, (int, float)):
            raise ValueError("average_temperature must be a number")
        self.__average_temperature = average_temperature

    # created with the help of GenAI
    def find_average_temperature(self):
        total_temp_min = 0
        total_temp_max = 0
        count = 0
        for weekly_forecast in self.main.weekly_forecasts:
            for daily_forecast in weekly_forecast.daily_forecasts.values():
                total_temp_min += daily_forecast.temperature_range['min']
                total_temp_max += daily_forecast.temperature_range['max']
                count += 1
        if count > 0:
            self.average_temperature = (total_temp_min + total_temp_max) / (2 * count)
        else:
            self.average_temperature = 0
        return self.average_temperature

######## test code ########
        
csv_file = "weather.csv"
file1 = Main(csv_file)

# Data analysis
data_analysis = DataAnalysis(file1)
print(data_analysis.find_average_temperature())

# Print the forecast for Brisbane
location_name = "Brisbane"
file1.location_print(location_name)