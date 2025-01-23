from enum import Enum

CITY_SQL_FILE = 'db\city.sql'
COUNTRY_SQL_FILE = 'db\country.sql'
COUNTRY_RECORD_SQL_FILE = 'db\country_record.sql'
GENERAL_WEATHER_SQL_FILE = 'db\general_weather.sql'
WEATHER_CONDITION_SQL_FILE = 'db\weather_condition.sql'
WEATHER_STATUS_SQL_FILE = 'db\weather_status.sql'

class CityEnableQueries(Enum):
    GET_BY_ID = 'GET BY ID'
    GET_ALL_BY_COUNTRY = 'GET ALL BY COUNTRY'
    INSERT = 'INSERT WITH UPDATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    DELETE_ALL_BY_COUNTRY = 'DELETE ALL BY COUNTRY'
    
class CountryEnableQueries(Enum):
    GET_BY_CODE = 'GET BY CODE'
    INSERT = 'INSERT WITH UPDATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    
class CountryRecordEnableQueries(Enum):
    GET_ALL_BY_COUNTRY_WITH_DATE_ORDER = 'GET ALL BY COUNTRY WITH DATE ORDER'
    INSERT = 'INSERT WITH UPDATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
