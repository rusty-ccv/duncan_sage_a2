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

class Location():
    def __init__(self, name):
        self.name = name
        
class WeeklyForecast():
   def __init__(self, upload_date):
      self.upload_date = upload_date

class DailyForcast(Location):
   def __init__(self, location, upload_date, forcast_date, temp_min, temp_max, condition, rainfall_possible, rainfall_chance, forecast, warning):
    self.location = location
    self.upload_date = upload_date
    self.forcast_dat = forcast_date
    self.temp_min = temp_min
    self.temp_max = temp_max
    self.condition = condition
    self.rainfall_possible = rainfall_possible
    self.rainfall_chance = rainfall_chance
    self.forecast = forecast
    self.warning = warning
    
    