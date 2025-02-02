import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)

from typing import Dict

import mysql.connector
from mysql.connector import Error

from db.sql_reader import SQLFileReader

class DAOException(Exception):
    def __init__(self, message):
        super().__init__(message)
        
class NotExistDataException(DAOException):
    def __init__(self, message = "Not found!"):
        super().__init__(message)
        
class BasicMySQLDAO:
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
                sql_file_path = os.path.join(init_dir, file)
                newFileReader.read(sql_file_path=sql_file_path)
                self._sqlFileReaders[file] = newFileReader
            except Exception as ioException:
                raise ioException
                
    def close_connection(self):
        self._connection.close()
