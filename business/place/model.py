import pycountry
from typing import Literal
from datetime import date, datetime

class Country:
    def __init__(self, code: str, name: str|None = None):
        self.code = code
        self.name = name
        
    @property
    def code(self):
        return self.__code
    
    @property
    def name(self):
        return self.__name
    
    @code.setter
    def code(self, code: str):
        try:
            if len(code) == 2:
                country_iso = pycountry.countries.get(alpha_2=code.upper())
            elif len(code) == 3:
                country_iso = pycountry.countries.get(alpha_3=code.upper())
            else:
                raise ValueError("Invalid country code!")
            self.__code = country_iso.alpha_2
        except ValueError as valueErr:
            raise ValueError("Invalid country code!")
        
    @name.setter
    def name(self, name: str|None):
        self.__name = name
            
    def get_code_with_type(self, code_type: Literal['alpha_2', 'alpha_3']) -> str:
        if self.__code is None:
            raise ValueError("Code is null!")
        try:
            country_iso = pycountry.countries.get(alpha_2=self.code)
            if code_type == 'alpha_2':
                return country_iso.alpha_2
            else:
                return country_iso.alpha_3
        except ValueError as e:
            raise e
        
    def get_iso_name(self) -> str:
        try:
            country_iso = pycountry.countries.get(alpha_2=self.__code)
            return country_iso.name
        except ValueError as e:
            raise e
        
    def get_offical_name(self) -> str:
        try:
            country_iso = pycountry.countries.get(alpha_2=self.__code)
            return country_iso.official_name
        except ValueError as e:
            raise e
        
    def __str__(self):
        s = f'Country('
        s += f'code={self.code}, '
        s += f'name={self.name}'
        s += f')'
        return s
    
class City:
    def __init__(self, city_id: int, 
                 name: str|None = None,
                 lat: float = 0.0,
                 lon: float = 0.0,
                 time_zone: int = 0,
                 country: Country|None = None):
        self.city_id = city_id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.time_zone = time_zone
        self.country = country
    
    @property
    def city_id(self):
        return self.__city_id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def lat(self):
        return self.__lat
    
    @property
    def lon(self):
        return self.__lon
    
    @property
    def time_zone(self):
        return self.__time_zone
    
    @property
    def country(self):
        return self.__country
    
    @city_id.setter
    def city_id(self, city_id: int):
        self.__city_id = city_id
        
    @name.setter
    def name(self, name: str|None):
        self.__name = name
    
    @lat.setter
    def lat(self, lat: float):
        self.__lat = lat
    
    @lon.setter
    def lon(self, lon: float):
        self.__lon = lon
    
    @time_zone.setter
    def time_zone(self, time_zone: int):
        if time_zone < -12 or time_zone > 14:
            raise ValueError("Time zone not in UTC-12 to UTC+14!")
        self.__time_zone = time_zone
    
    @country.setter
    def country(self, country: Country|None):
        self.__country = country
    
    def __str__(self):
        s = f'City('
        s += f'city_id={self.city_id}, '
        s += f'name={self.name}, '
        s += f'lat={self.lat:.2f}, '
        s += f'lon={self.lon:.2f}, '
        s += f'time_zon=UTC{"+" if self.time_zone>=0 else "-"}{self.time_zone}, '
        s += f'country={self.country}'
        s += f')'
        return s
    
class CountryRecord:
    def __init__(self, country: Country, 
                 collect_date: date = date.today(),
                 sunrise: datetime|None = None,
                 sunset: datetime|None = None):
        self.country = country
        self.collect_date = collect_date
        self.sunrise = sunrise
        self.sunset = sunset
    
    @property
    def country(self):
        return self.__country
    
    @property
    def collect_date(self):
        return self.__collect_date
    
    @property
    def sunrise(self):
        return self.__sunrise
    
    @property
    def sunset(self):
        return self.__sunset
    
    @country.setter
    def country(self, country: Country):
        self.__country = country
        
    @collect_date.setter
    def collect_date(self, collect_date: date = date.today()):
        self.__collect_date = collect_date
    
    @sunrise.setter
    def sunrise(self, sunrise: datetime|None = None):
        self.__sunrise = sunrise
        
    @sunset.setter
    def sunset(self, sunset: datetime|None = None):
        self.__sunset = sunset
        
    def __str__(self):
        s = f'CountryRecord('
        s += f'country={self.country}, '
        s += f'collect_date={self.collect_date}, '
        s += f'sunrise={self.sunrise}, '
        s += f'sunset={self.sunset}'
        s += f')'
        return s

if __name__ == '__main__':
    vietnam = Country('VN')
    hanoi = City(1, 'Ha Noi', 123.5, 95.4, 7, vietnam)
    print(vietnam)
    print(hanoi)
    vietnam_today = CountryRecord(vietnam, date.today(), datetime(2025, 1, 20, 6, 1, 30), datetime.now())
    print(vietnam_today)