import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)

from mysql.connector import Error

from typing import List
from abc import ABC, abstractmethod

from model import GeneralWeather, WeatherStatus
import db.info as dbinfo

from common.dao import BasicMySQLDAO, DAOException, NotExistDataException

class BasicGeneralWeatherDAO(ABC):
    
    @abstractmethod
    def get(self, status_id: int) -> GeneralWeather:
        pass
    
    @abstractmethod
    def get_all(self) -> list[GeneralWeather]:
        pass
    
class MySQLGeneralWeatherDAO(BasicMySQLDAO, BasicGeneralWeatherDAO):
    def __init__(self, host, db, user, password):
        super().__init__(host, db, user, password,
                         queriesFile=dbinfo.GENERAL_WEATHER_SQL_FILE)
        self._general_weather_reader = self._sqlFileReaders[dbinfo.GENERAL_WEATHER_SQL_FILE]
        
    def get(self, status_id: int) -> GeneralWeather:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        
        get_status_query = self._general_weather_reader.get_query_of(
            dbinfo.GeneralWeatherEnableQueries.GET_BY_STATUS.value
        )
        
        try:
            cursor.execute(get_status_query, (status_id, ))
            get_general_weather_result = cursor.fetchone()
            if get_general_weather_result is None:
                raise NotExistDataException()
            return GeneralWeather.from_tuple(source=get_general_weather_result)
        except Error as e:
            raise DAOException(e.msg)
        finally:
            cursor.close()
            
    def get_all(self) -> list[GeneralWeather]:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor()
        
        get_status_query = self._general_weather_reader.get_query_of(
            dbinfo.GeneralWeatherEnableQueries.GET_ALL_STATUS.value
        )
        
        try:
            cursor.execute(get_status_query)
            get_general_weather_results = cursor.fetchall()
            results: List[GeneralWeather] = []
            for result in get_general_weather_results:
                results.append(GeneralWeather.from_tuple(source=result))
            return results
        except Error as e:
            raise DAOException(e.msg)
        finally:
            cursor.close()
            
if __name__ == '__main__':
    dao = MySQLGeneralWeatherDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
    for item in dao.get_all():
        print(item)
    