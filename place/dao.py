import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)

from mysql.connector import Error

from typing import List
from abc import ABC, abstractmethod

from model import Country, City
import db.info as dbinfo

from common.dao import BasicMySQLDAO, DAOException, NotExistDataException

class BasicCountryDAO(ABC):
    
    @abstractmethod
    def get(self, code: str) -> Country:
        pass
    
    @abstractmethod
    def insert(self, new_country: Country) -> None:
        pass
    
    @abstractmethod
    def delete(self, code: str) -> None:
        pass

class MySQLCountryDAO(BasicMySQLDAO, BasicCountryDAO):
    def __init__(self, host, db, user, password):
        super().__init__(host, db, user, password,
                         queriesFile=dbinfo.COUNTRY_SQL_FILE)
        self._country_reader = self._sqlFileReaders[dbinfo.COUNTRY_SQL_FILE]
    
    def get(self, code: str) -> Country:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        get_country_query = self._country_reader.get_query_of(
            dbinfo.CountryEnableQueries.GET_BY_CODE.value
        )
        country = Country(code)
        code = country.code
        try:
            cursor.execute(get_country_query, (code, ))
            get_country_result = cursor.fetchone()
            if get_country_result is None:
                raise NotExistDataException()

            return Country.from_tuple(source=get_country_result)
        except Error as e:
            raise DAOException(e.msg)
        finally:
            cursor.close()
        
    def insert(self, new_country: Country) -> None:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        insert_country_query = self._country_reader.get_query_of(
            dbinfo.CountryEnableQueries.INSERT.value
        )
        try:
            cursor.execute(insert_country_query, (new_country.code, new_country.name))
            self._connection.commit()
        except Error as e:
            if self._connection.is_connected():
                self._connection.rollback()
            raise DAOException(e.msg)
        finally:
            cursor.close()
    
    def delete(self, code: str) -> None:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        delete_query = self._country_reader.get_query_of(
            dbinfo.CountryEnableQueries.DELETE.value
        )
        country = Country(code)
        code = country.code
        try:
            cursor.execute(delete_query, (code, ))
            self._connection.commit()
        except Error as e:
            if self._connection.is_connected():
                self._connection.rollback()
            raise DAOException(e.msg)
        finally:
            cursor.close()

class BasicCityDAO(ABC):
    
    @abstractmethod
    def get(self, city_id: int|None = None, city_name: str|None = None) -> City:
        pass
    
    @abstractmethod
    def insert(self, new_city: City) -> None:
        pass
    
    @abstractmethod
    def delete(self, city_id: int) -> None:
        pass
    
    @abstractmethod
    def get_all(self, country_code: str) -> list[City]:
        pass

class MySQLCityDAO(BasicMySQLDAO):
    def __init__(self, host, db, user, password):
        super().__init__(host, db, user, password,
                         queriesFile=[dbinfo.COUNTRY_SQL_FILE,
                                      dbinfo.CITY_SQL_FILE])
        self._country_reader = self._sqlFileReaders[dbinfo.COUNTRY_SQL_FILE]
        self._city_reader = self._sqlFileReaders[dbinfo.CITY_SQL_FILE]
        
    def get(self, city_id: int|None = None, city_name: str|None = None) -> City:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        if city_id is None and city_name is None:
            raise NotExistDataException()
        
        cursor = self._connection.cursor(prepared=True)
        get_country_query = self._country_reader.get_query_of(
            dbinfo.CountryEnableQueries.GET_BY_CODE.value
        )
        get_city_query = self._city_reader.get_query_of(
            dbinfo.CityEnableQueries.GET_BY_ID.value
        )
        get_city_name_query = self._city_reader.get_query_of(
            dbinfo.CityEnableQueries.GET_BY_NAME.value
        )

        try:
            if city_id is not None:
                cursor.execute(get_city_query, (city_id, ))
                get_city_result = cursor.fetchone()
            else:
                cursor.execute(get_city_name_query, (city_name, ))
                get_city_result = cursor.fetchone()
            if get_city_result is None:
                raise NotExistDataException()
            country_code = get_city_result[5]
            cursor.execute(get_country_query, (country_code, ))
            get_country_result = cursor.fetchone()
            if get_country_result is None:
                raise NotExistDataException()

            country_source = get_country_result
            source = get_city_result[:-1] + (country_source, )

            return City.from_tuple(source)
        except Error as e:
            raise DAOException(e.msg)
        finally:
            cursor.close()
            
    def insert(self, new_city: City) -> None:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        insert_country_query = self._country_reader.get_query_of(
            dbinfo.CountryEnableQueries.INSERT.value
        )
        insert_city_query = self._city_reader.get_query_of(
            dbinfo.CityEnableQueries.INSERT.value
        )
        try:
            new_country = new_city.country
            if new_country is not None:
                cursor.execute(insert_country_query, (new_country.code, new_country.name))
            cursor.execute(insert_city_query, new_city.to_tuple()[:-1] + (new_country.code, ))
            self._connection.commit()
        except Error as e:
            if self._connection.is_connected():
                self._connection.rollback()
            raise DAOException(e.msg)
        finally:
            cursor.close()
    
    def delete(self, city_id: int) -> None:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        delete_query = self._city_reader.get_query_of(
            dbinfo.CityEnableQueries.DELETE.value
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
        
    def get_all(self, country_code: str) -> list[City]:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        get_country_query = self._country_reader.get_query_of(
            dbinfo.CountryEnableQueries.GET_BY_CODE.value
        )
        get_city_query = self._city_reader.get_query_of(
            dbinfo.CityEnableQueries.GET_ALL_BY_COUNTRY.value
        )

        try:
            cursor.execute(get_city_query, (country_code, ))
            get_city_results = cursor.fetchall()
            cursor.execute(get_country_query, (country_code, ))
            get_country_result = cursor.fetchone()
            country_source = get_country_result
            citys: List[City] = []
            for city_result in get_city_results:        
                source = city_result[:-1] + (country_source, )
                citys.append(City.from_tuple(source))

            return citys
        except Error as e:
            raise DAOException(e.msg)
        finally:
            cursor.close()
            
if __name__ == '__main__':
    cityDAO = MySQLCityDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
    citys = cityDAO.get_all('VN')
    for city in citys:
        print(city.lat is None)
    