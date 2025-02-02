from typing import Literal
from datetime import datetime
class GeneralWeather:
    def __init__(self, status_id: int, description: str|None = None):
        self.status_id = status_id
        self.description = description
    
    @property
    def status_id(self):
        return self.__status_id
    
    @property
    def description(self):
        return self.__description
    
    @status_id.setter
    def status_id(self, status_id: int):
        self.__status_id = status_id
    
    @description.setter
    def description(self, description: str|None):
        self.__description = description
    
    def __str__(self):
        s = f'GeneralWeather('
        s += f'status_id={self.__status_id}, '
        s += f'description={self.__description}'
        s += f')'
        return s
    
    def from_tuple(source: tuple[int, str|None]) -> 'GeneralWeather':
        if len(source) == 0:
            return None
        if len(source) != 2:
            raise ValueError("Invalid argurment, required 2 argument!")
        return GeneralWeather(
            status_id=source[0],
            description=source[1]
        )
    
    def to_tuple(self) -> tuple[int, str|None]:
        return self.__status_id, self.__description
    
from datetime import datetime

class WeatherStatus:
    def __init__(self, city_id: int, collect_time: datetime,
                 temp: float|None = None, feels_temp: float|None = None,
                 pressure: int|None = None, humidity: int|None = None,
                 sea_level: int|None = None, grnd_level: int|None = None,
                 visibility: int|None = None, wind_speed: float|None = None,
                 wind_deg: int|None = None, wind_gust: float|None = None,
                 clouds_all: int|None = None, rain: float|None = None,
                 sunrise: datetime|None = None, sunset: datetime|None = None,
                 aqi: int|None = None, pm2_5: float|None = None,
                 general_weathers: list[GeneralWeather] = []):
        self.city_id = city_id
        self.collect_time = collect_time
        self.temp = temp
        self.feels_temp = feels_temp
        self.pressure = pressure
        self.humidity = humidity
        self.sea_level = sea_level
        self.grnd_level = grnd_level
        self.visibility = visibility
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg
        self.wind_gust = wind_gust
        self.clouds_all = clouds_all
        self.rain = rain
        self.sunrise = sunrise
        self.sunset = sunset
        self.aqi = aqi
        self.pm2_5 = pm2_5
        self.general_weathers = general_weathers

    @property
    def city_id(self):
        return self.__city_id
    
    @property
    def collect_time(self):
        return self.__collect_time

    @property
    def temp(self):
        return self.__temp
    
    @property
    def feels_temp(self):
        return self.__feels_temp

    @property
    def pressure(self):
        return self.__pressure
    
    @property
    def humidity(self):
        return self.__humidity
    
    @property
    def sea_level(self):
        return self.__sea_level

    @property
    def grnd_level(self):
        return self.__grnd_level
    
    @property
    def visibility(self):
        return self.__visibility
    
    @property
    def wind_speed(self):
        return self.__wind_speed
    
    @property
    def wind_deg(self):
        return self.__wind_deg
    
    @property
    def wind_gust(self):
        return self.__wind_gust
    
    @property
    def clouds_all(self):
        return self.__clouds_all
    
    @property
    def rain(self):
        return self.__rain
    
    @property
    def sunrise(self):
        return self.__sunrise
    
    @property
    def sunset(self):
        return self.__sunset
    
    @property
    def aqi(self):
        return self.__aqi
    
    @property
    def pm2_5(self):
        return self.__pm2_5
    
    @property
    def general_weathers(self):
        return self.__general_weathers

    @city_id.setter
    def city_id(self, city_id: int):
        self.__city_id = city_id
    
    @collect_time.setter
    def collect_time(self, collect_time: datetime):
        self.__collect_time = collect_time

    @temp.setter
    def temp(self, temp: float|None):
        self.__temp = temp
    
    @feels_temp.setter
    def feels_temp(self, feels_temp: float|None):
        self.__feels_temp = feels_temp

    @pressure.setter
    def pressure(self, pressure: int|None):
        self.__pressure = pressure
    
    @humidity.setter
    def humidity(self, humidity: int|None):
        self.__humidity = humidity
    
    @sea_level.setter
    def sea_level(self, sea_level: int|None):
        self.__sea_level = sea_level

    @grnd_level.setter
    def grnd_level(self, grnd_level: int|None):
        self.__grnd_level = grnd_level
    
    @visibility.setter
    def visibility(self, visibility: int|None):
        self.__visibility = visibility
    
    @wind_speed.setter
    def wind_speed(self, wind_speed: float|None):
        self.__wind_speed = wind_speed
    
    @wind_deg.setter
    def wind_deg(self, wind_deg: int|None):
        self.__wind_deg = wind_deg
    
    @wind_gust.setter
    def wind_gust(self, wind_gust: float|None):
        self.__wind_gust = wind_gust
    
    @clouds_all.setter
    def clouds_all(self, clouds_all: int|None):
        self.__clouds_all = clouds_all
    
    @rain.setter
    def rain(self, rain: float|None):
        self.__rain = rain
    
    @sunrise.setter
    def sunrise(self, sunrise: datetime|None):
        self.__sunrise = sunrise
    
    @sunset.setter
    def sunset(self, sunset: datetime|None):
        self.__sunset = sunset
    
    @aqi.setter
    def aqi(self, aqi: int|None):
        self.__aqi = aqi
    
    @pm2_5.setter
    def pm2_5(self, pm2_5: float|None):
        self.__pm2_5 = pm2_5
        
    @general_weathers.setter
    def general_weathers(self, general_weathers: list[GeneralWeather] = []):
        self.__general_weathers = general_weathers

    def __str__(self):
        s = f'WeatherStatus('
        s += f'city_id={self.__city_id},' 
        s += f'collect_time={self.__collect_time}, '
        s += f'temp={self.__temp}, '
        s += f'feels_temp={self.__feels_temp}, '
        s += f'pressure={self.__pressure}, '
        s += f'humidity={self.__humidity}, '
        s += f'sea_level={self.__sea_level}, '
        s += f'grnd_level={self.__grnd_level}, '
        s += f'visibility={self.__visibility}, '
        s += f'wind_speed={self.__wind_speed}, '
        s += f'wind_deg={self.__wind_deg}, '
        s += f'wind_gust={self.__wind_gust}, '
        s += f'clouds_all={self.__clouds_all}, '
        s += f'rain={self.__rain}, '
        s += f'sunrise={self.__sunrise}, '
        s += f'sunset={self.__sunset}, '
        s += f'aqi={self.__aqi}, ' 
        s += f'pm2_5={self.__pm2_5}'
        s += f'general_weathers=[{", ".join(str(general_weather) for general_weather in self.__general_weathers)}]'
        s += ')'
        return s

    def from_tuple(source: tuple) -> 'WeatherStatus':
        if len(source) == 0:
            return None
        if len(source) != 19:
            raise ValueError("Invalid argument, required 19 arguments!")
        return WeatherStatus(
            city_id=source[0],
            collect_time=source[1],
            temp=source[2],
            feels_temp=source[3],
            pressure=source[4],
            humidity=source[5],
            sea_level=source[6],
            grnd_level=source[7],
            visibility=source[8],
            wind_speed=source[9],
            wind_deg=source[10],
            wind_gust=source[11],
            clouds_all=source[12],
            rain=source[13],
            sunrise=source[14],
            sunset=source[15],
            aqi=source[16],
            pm2_5=source[17],
            general_weathers=source[18]
        )

    def to_tuple(self) -> tuple:
        return (self.__city_id, self.__collect_time, self.__temp, self.__feels_temp, self.__pressure, 
                self.__humidity, self.__sea_level, self.__grnd_level, self.__visibility, self.__wind_speed, 
                self.__wind_deg, self.__wind_gust, self.__clouds_all, self.__rain, self.__sunrise, 
                self.__sunset, self.__aqi, self.__pm2_5, self.__general_weathers)

        