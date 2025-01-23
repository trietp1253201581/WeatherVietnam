import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import mysql.connector
from mysql.connector import Error

from typing import Dict

from model import Country, City, CountryRecord
from db.sql_reader import SQLFileReader
import db.info as dbinfo

class DAOException(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class NotExistDataException(DAOException):

   def __init__(self, message = "Not found!"):
        super().__init__(message)
        
class BasicPlaceDAO:
    def __init__(self, host: str, db: str, user: str, password: str, queriesFile: str|list[str]|None = None):
        self.connect_(host, db, user, password)
        self._sqlFileReaders: Dict[str, SQLFileReader] = {}
        self.get_sql_file_reader_(queriesFile)
        
    def connect_(self, host: str, db: str, user: str, password: str):
        try:
            self._connection = mysql.connector.connect(
                host=host,
                database=db,
                user=user,
                password=password
            )              
        except Error as ex:
            print("Error", ex)
            raise DAOException(ex.msg)
        
    def get_sql_file_reader_(self, queriesFile: str|list[str]|None):
        if queriesFile is None:
            return
        if isinstance(queriesFile, str):
            queriesFiles = [queriesFile]
        else:
            queriesFiles = queriesFile
        for file in queriesFiles:
            try:
                newFileReader = SQLFileReader()
                init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
                sql_file_path = os.path.join(init_dir, file)
                newFileReader.read(sql_file_path=sql_file_path)
                self._sqlFileReaders[file] = newFileReader
            except Exception as ioException:
                raise ioException
                
    def close_connection(self):
        self._connection.close()

class CountryDAO(BasicPlaceDAO):
    
    def __init__(self, host, db, user, password):
        super().__init__(host, db, user, password,
                         queriesFile=[dbinfo.COUNTRY_SQL_FILE,
                                      dbinfo.COUNTRY_RECORD_SQL_FILE])
        self._country_reader = self._sqlFileReaders[dbinfo.COUNTRY_SQL_FILE]
        self._country_record_reader = self._sqlFileReaders[dbinfo.COUNTRY_RECORD_SQL_FILE]
    
    def get(self, code: str) -> Country:
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        
        cursor = self._connection.cursor(prepared=True)
        get_country_query = self._country_reader.get_query_of(
            dbinfo.CountryEnableQueries.GET_BY_CODE.value
        )
        get_country_record_query = self._country_record_reader.get_query_of(
            dbinfo.CountryRecordEnableQueries.GET_ALL_BY_COUNTRY_WITH_DATE_ORDER.value
        )
        country = Country(code)
        code = country.code
        try:
            cursor.execute(get_country_query, (code, ))
            get_country_result = cursor.fetchone()
            if get_country_result is None:
                raise NotExistDataException()
            cursor.execute(get_country_record_query, (code, ))
            get_country_record_result = cursor.fetchall()
            source = get_country_result + ([(tup[1], tup[2], tup[3]) for tup in get_country_record_result], )

            return Country.from_tuple(source)
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
        insert_country_record_query = self._country_record_reader.get_query_of(
            dbinfo.CountryRecordEnableQueries.INSERT.value
        )
        try:
            cursor.execute(insert_country_query, (new_country.code, new_country.name))
            for record in new_country.records:
                cursor.execute(insert_country_record_query, (
                    new_country.code,
                    record.collect_date,
                    record.sunrise,
                    record.sunset
                ))
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

