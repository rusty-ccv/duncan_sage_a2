#Duncan Sage - 24034122

# Your job is to write an object-oriented program in Python with a minimum of five classes that:
# • Reads the data in the csv file and uses the data to create appropriate objects.
# • Stores all of the objects in appropriate collection(s).
# • Uses a Set to perform some basic data analysis.
# Thing to think about:
# • How will you handle and manipulate the strings in the csv file?
# • How will you structure your classes and what relationships will the classes contain?
# • What attributes should each class have and what data type should they be?
# • How will you secure and validate the data in each class?
# • How will you handle any potential errors in your program?
# Two possible ways to approach the problem may be to:
# • Have a forecast class with attributes for individual items in each forecast.
# • Have an observation class and view the individual items in each forecast as an observation (similar to
# the sample project used in the Live Coding sessions)

#Location,Updated Date,Forecast Date,Min Temp,Max Temp,Condition,Possible Rainfall,Chance of any Rain,Forecast,Warning

import csv

#class Attribute getters and setters used genAI to copy from hand written code
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
    def __init__(self, location_name, upload_date, forecast_date, temperature_range, 
                 condition, rainfall_possible, rainfall_chance, forecast, warning):
        super().__init__(location_name)
        self.upload_date = upload_date
        self.forecast_date = forecast_date
        self.temperature_range = temperature_range
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
        if not isinstance(upload_date, str):
            raise ValueError("upload_date must be a string")
        self._upload_date = upload_date

    @property
    def forecast_date(self):
        return self._forecast_date
    
    @forecast_date.setter
    def forecast_date(self, forecast_date):
        if not isinstance(forecast_date, str):
            raise ValueError("forecast_date must be a string")
        self._forecast_date = forecast_date
    
    @property
    def temperature_range(self):
        return self._temperature_range
    
    @temperature_range.setter
    def temperature_range(self, temperature_range):
        if not isinstance(temperature_range, dict):
            raise ValueError("temperature_range must be a dictionary")
        self._temperature_range = temperature_range

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
        return (self.location_name, self.upload_date, self.forecast_date, self.temperature_range, self.temperature_range, 
                self.condition, self.rainfall_possible, self.rainfall_chance, self.forecast, self.warning)
        
class DailyForecast(Forecast):
    pass

class WeeklyForecast:
    def __init__(self, upload_date):
        self.upload_date = upload_date
        self.daily_forecasts = {}

    @property
    def upload_date(self):
        return self._upload_date
    
    @upload_date.setter
    def upload_date(self, upload_date):
        if not isinstance(upload_date, str):
            raise ValueError("upload_date must be a string")
        self._upload_date = upload_date

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

class CsvReader:
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
    def __init__(self, file_name):
        self.file_name = file_name
        self.weekly_forecasts = []
        csv_reader = CsvReader(self)
        csv_reader.read_csv(self.file_name)

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
    def __init__(self, main):
        self.main = main
        self._average_temperature = 0
    
    @property
    def average_temperature(self):
        return self._average_temperature
    
    @average_temperature.setter
    def average_temperature(self, average_temperature):
        if not isinstance(average_temperature, (int, float)):
            raise ValueError("average_temperature must be a number")
        self._average_temperature = average_temperature

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

# Print the contents of the file
data_analysis = DataAnalysis(file1)
print(data_analysis.find_average_temperature())

# Print the forecast for Brisbane
location_name = "Brisbane"
file1.location_print(location_name)