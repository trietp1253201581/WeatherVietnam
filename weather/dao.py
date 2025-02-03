import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)

from mysql.connector import Error

from typing import List
from abc import ABC, abstractmethod
from datetime import datetime

from weather.model import GeneralWeather, WeatherStatus
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
            
class BasicWeatherStatusDAO(ABC):
    
    @abstractmethod
    def get(self, city_id: int, collect_time: datetime) -> WeatherStatus:
        pass
    
    @abstractmethod
    def get_all(self, city_id: int) -> list[WeatherStatus]:
        pass
    
    @abstractmethod
    def insert(self, new_weather: WeatherStatus) -> None:
        pass
    
    @abstractmethod
    def delete(self, city_id: int, collect_time: datetime) -> None:
        pass
    
    @abstractmethod
    def delete_all(self, city_id: int) -> None:
        pass
    
class MySQLWeatherStatusDAO(BasicMySQLDAO, BasicWeatherStatusDAO):
    def __init__(self, host, db, user, password):
        super().__init__(host, db, user, password,
                         queriesFile=[dbinfo.GENERAL_WEATHER_SQL_FILE,
                                      dbinfo.WEATHER_STATUS_SQL_FILE,
                                      dbinfo.WEATHER_CONDITION_SQL_FILE])
        self._general_weather_reader = self._sqlFileReaders[dbinfo.GENERAL_WEATHER_SQL_FILE]
        self._weather_status_reader = self._sqlFileReaders[dbinfo.WEATHER_STATUS_SQL_FILE]
        self._weather_condition_reader = self._sqlFileReaders[dbinfo.WEATHER_CONDITION_SQL_FILE]
            
    def get(self, city_id: int, collect_time: datetime) -> WeatherStatus:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        
        get_status_query = self._general_weather_reader.get_query_of(
            dbinfo.GeneralWeatherEnableQueries.GET_BY_STATUS.value
        )      
        get_weather_query = self._weather_status_reader.get_query_of(
            dbinfo.WeatherStatusEnableQueries.GET_BY_CITY_AND_TIME.value
        )
        get_condition_query = self._weather_condition_reader.get_query_of(
            dbinfo.WeatherConditionEnableQueries.GET_ALL_BY_CITY_AND_TIME.value
        )
        
        try:
            cursor.execute(get_weather_query, (city_id, collect_time))
            get_weather_result = cursor.fetchone()
            if get_weather_result is None:
                raise NotExistDataException()
            cursor.execute(get_condition_query, (city_id, collect_time))
            conditions: List[tuple] = []
            get_condition_results = cursor.fetchall()
            for get_condition_result in get_condition_results:
                status_id = get_condition_result[2]
                cursor.execute(get_status_query, (status_id, ))
                conditions.append(cursor.fetchone())
            source = get_weather_result + (conditions, )
            return WeatherStatus.from_tuple(source)
        except Error as e:
            raise DAOException(e.msg)
        finally:
            cursor.close()
            
    def get_all(self, city_id: int) -> list[WeatherStatus]:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        
        get_status_query = self._general_weather_reader.get_query_of(
            dbinfo.GeneralWeatherEnableQueries.GET_BY_STATUS.value
        )      
        get_weather_query = self._weather_status_reader.get_query_of(
            dbinfo.WeatherStatusEnableQueries.GET_ALL_BY_CITY.value
        )
        get_condition_query = self._weather_condition_reader.get_query_of(
            dbinfo.WeatherConditionEnableQueries.GET_ALL_BY_CITY_AND_TIME.value
        )
        
        try:
            cursor.execute(get_weather_query, (city_id, ))
            get_weather_results = cursor.fetchall()
            weather_statuses: List[WeatherStatus] = []
            for get_weather_result in get_weather_results:
                collect_time = get_weather_result[1]
                cursor.execute(get_condition_query, (city_id, collect_time))
                conditions: List[tuple] = []
                get_condition_results = cursor.fetchall()
                for get_condition_result in get_condition_results:
                    status_id = get_condition_result[2]
                    cursor.execute(get_status_query, (status_id, ))
                    conditions.append(cursor.fetchone())
                source = get_weather_result + (conditions, )
                weather_statuses.append(WeatherStatus.from_tuple(source))
            return weather_statuses
        except Error as e:
            raise DAOException(e.msg)
        finally:
            cursor.close()
    
    def insert(self, new_weather: WeatherStatus) -> None:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        
        insert_status_query = self._weather_status_reader.get_query_of(
            dbinfo.WeatherStatusEnableQueries.INSERT.value
        )
        insert_condition_query = self._weather_condition_reader.get_query_of(
            dbinfo.WeatherConditionEnableQueries.INSERT.value
        )
        delete_condition_query = self._weather_condition_reader.get_query_of(
            dbinfo.WeatherConditionEnableQueries.DELETE.value
        )
        
        try:
            cursor.execute(insert_status_query, new_weather.to_tuple()[:-1])
            cursor.execute(delete_condition_query, (new_weather.city_id, new_weather.collect_time))
            for general_weather in new_weather.general_weathers:
                cursor.execute(insert_condition_query, (
                    new_weather.city_id, new_weather.collect_time, general_weather.status_id
                ))
            self._connection.commit()
        except Error as e:
            if self._connection.is_connected():
                self._connection.rollback()
            raise DAOException(e.msg)
        finally:
            cursor.close()
            
    def delete(self, city_id: int, collect_time: datetime) -> None:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        
        delete_query = self._weather_status_reader.get_query_of(
            dbinfo.WeatherStatusEnableQueries.DELETE.value
        )
        
        try:
            cursor.execute(delete_query, (city_id, collect_time))
            self._connection.commit()
        except Error as e:
            if self._connection.is_connected():
                self._connection.rollback()
            raise DAOException(e.msg)
        finally:
            cursor.close()
    
    def delete_all(self, city_id):
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        
        delete_query = self._weather_status_reader.get_query_of(
            dbinfo.WeatherStatusEnableQueries.DELETE_ALL_BY_CITY.value
        )
        
        try:
            cursor.execute(delete_query, (city_id, ))
            self._connection.commit()
        except Error as e:
            if self._connection.is_connected():
                self._connection.rollback()
            raise DAOException(e.msg)
        finally:
            cursor.close()
         
if __name__ == '__main__':
    dao = MySQLWeatherStatusDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
    
    for weather in dao.get_all(1):
        print(weather)