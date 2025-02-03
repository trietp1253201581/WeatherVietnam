import pycountry
from typing import Literal

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
        s += f'code={self.__code}, '
        s += f'name={self.__name}'
        s += f')'
        return s
    
    @staticmethod
    def from_tuple(source: tuple[str, str|None]) -> 'Country':
        if len(source) == 0:
            return None
        if len(source) != 2:
            raise ValueError("Invalid argurment, required 2 argument!")
        return Country(
            code=source[0],
            name=source[1]
        )
    
    def to_tuple(self) -> tuple[str, str|None]:
        return self.__code, self.__name
    
class City:
    def __init__(self, city_id: int, 
                 name: str|None = None,
                 lon: float = 0.0,
                 lat: float = 0.0,       
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
        
    def get_coord(self) -> tuple[float, float]:
        return self.__lon, self.__lat
    
    def __str__(self):
        s = f'City('
        s += f'city_id={self.city_id}, '
        s += f'name={self.name}, '
        s += f'lon={self.lon:.2f}, ' if self.lon is not None else 'lon=None, '
        s += f'lat={self.lat:.2f}, ' if self.lat is not None else 'lat=None, '
        s += f'time_zone=UTC{"+" if self.time_zone>=0 else "-"}{abs(self.time_zone)}, '
        s += f'country={self.country}'
        s += f')'
        return s
    
    @staticmethod
    def from_tuple(source: tuple[int, str|None, float, float, int, tuple]) -> 'City':
        if len(source) == 0:
            return None
        if len(source) != 6:
            raise ValueError("Invalid argurment, required 6 argument!")
        return City(
            city_id=source[0],
            name=source[1],
            lon=source[2],
            lat=source[3],
            time_zone=source[4],
            country=Country.from_tuple(source[5])
        )
        
    def to_tuple(self) -> tuple[int, str|None, float, float, int, tuple]:
        return self.__city_id, self.__name, self.__lon, self.__lat, self.__time_zone, self.__country.to_tuple()