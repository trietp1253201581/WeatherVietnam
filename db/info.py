"""
Module `info` cung cấp đường dẫn tới các file `.sql` cần thiết
và các hằng đại diện cho các loại câu lệnh có thể thao tác với 1
bảng trong CSDL.

Author: 
    Lê Minh Triết
Last Modified Date: 
    03/02/2025
"""

from enum import Enum

CITY_SQL_FILE = 'db\city.sql'
COUNTRY_SQL_FILE = 'db\country.sql'
COUNTRY_RECORD_SQL_FILE = 'db\country_record.sql'
GENERAL_WEATHER_SQL_FILE = 'db\general_weather.sql'
WEATHER_CONDITION_SQL_FILE = 'db\weather_condition.sql'
WEATHER_STATUS_SQL_FILE = 'db\weather_status.sql'

class CityEnableQueries(Enum):
    GET_BY_ID = 'GET BY ID'
    GET_BY_NAME = 'GET BY NAME'
    GET_ALL_BY_COUNTRY = 'GET ALL BY COUNTRY'
    INSERT = 'INSERT WITH UPDATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    DELETE_ALL_BY_COUNTRY = 'DELETE ALL BY COUNTRY'
    
class CountryEnableQueries(Enum):
    GET_BY_CODE = 'GET BY CODE'
    INSERT = 'INSERT WITH UPDATE'
    DELETE = 'DELETE'
    
class GeneralWeatherEnableQueries(Enum):
    GET_BY_STATUS = 'GET BY STATUS'
    GET_ALL_STATUS = 'GET ALL STATUS'
    
class WeatherStatusEnableQueries(Enum):
    GET_BY_CITY_AND_TIME = 'GET BY CITY AND TIME'
    GET_ALL_BY_CITY = 'GET ALL BY CITY'
    INSERT = 'INSERT'
    DELETE = 'DELETE'
    DELETE_ALL_BY_CITY = 'DELETE ALL BY CITY'
    
class WeatherConditionEnableQueries(Enum):
    GET_ALL_BY_CITY_AND_TIME = 'GET ALL BY CITY AND TIME'
    INSERT = 'INSERT'
    DELETE = 'DELETE'