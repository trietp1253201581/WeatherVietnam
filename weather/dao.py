"""
Module `dao` cung cấp các DAO để thao tác CSDL
của các general_weather và weather_status.

Author: 
    Lê Minh Triết
Last Modified Date: 
    04/02/2025
"""

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
from common.dao import BasicMySQLDAO, DAOException, NotExistDataException, BasicMongoDBDAO

class BasicGeneralWeatherDAO(ABC):
    """
    Cung cấp các phương thức có thể thao tác trên CSDL các general weather.
    Các class phải thực thi các phương thức trừu tượng này.
    """
    
    @abstractmethod
    def get(self, status_id: int) -> GeneralWeather:
        """
        Lấy một kiểu thời tiết chung dựa vào mã định danh của kiểu.

        Args:
            status_id (int): ID của kiểu thời tiết

        Returns:
            GeneralWeather: Kiểu thời tiết thu được
        """
        pass
    
    @abstractmethod
    def get_all(self) -> list[GeneralWeather]:
        """
        Lấy danh sách tất cả các kiểu thời tiết được lưu trong CSDL

        Returns:
            list[GeneralWeather]: Danh sách các kiểu thời tiết chung
        """
        pass
    
class MySQLGeneralWeatherDAO(BasicMySQLDAO, BasicGeneralWeatherDAO):
    """
    Triển khai các phương thức thao tác với CSDL của các general weather 
    trên CSDL MySQL.
    """
    
    def __init__(self, host, db, user, password):
        """
        Khởi tạo một DAO. Đường dẫn tới Queries file được thêm vào từ `db.info`.
        
        Args:
            host (str): Máy chủ CSDL. Nếu bạn sử dụng localhost (địa chỉ loopback) 
                thì hãy truyền vào giá trị `host='localhost'`.
            db (str): Tên của CSDL.
            user (str): Tên đăng nhập để truy cập vào CSDL, thông thường là `'root'`.
            password (str): Mật khẩu bạn dùng để truy cập CSDL với tên đăng nhập trên.
        """
        super().__init__(host, db, user, password,
                         queriesFile=dbinfo.GENERAL_WEATHER_SQL_FILE)
        self._general_weather_reader = self._sqlFileReaders[dbinfo.GENERAL_WEATHER_SQL_FILE]
        
    def get(self, status_id: int) -> GeneralWeather:
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy các query
        get_status_query = self._general_weather_reader.get_query_of(
            dbinfo.GeneralWeatherEnableQueries.GET_BY_STATUS.value
        )
        
        # Lấy dữ liệu
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
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor()
        
        # Lấy query
        get_status_query = self._general_weather_reader.get_query_of(
            dbinfo.GeneralWeatherEnableQueries.GET_ALL_STATUS.value
        )
        
        # Lấy dữ liệu
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
    """
    Cung cấp các phương thức có thể thao tác trên CSDL các weather status của các city.
    Các class phải thực thi các phương thức trừu tượng này.
    """
    
    @abstractmethod
    def get(self, city_id: int, collect_time: datetime) -> WeatherStatus:
        """
        Lấy trạng thái thời tiết của một thành phố tại một thời điểm xác định.

        Args:
            city_id (int): Mã định danh của thành phố
            collect_time (datetime): Thời điểm cần lấy dữ liệu thời tiết

        Returns:
            WeatherStatus: Trạng thái thời tiết thu được (nếu không tìm được thì ném ngoại lệ)
        """
        pass
    
    @abstractmethod
    def get_all(self, city_id: int) -> list[WeatherStatus]:
        """
        Lấy tất cả các trạng thái thời tiết của một thành phố từ lúc thu thập dữ liệu

        Args:
            city_id (int): Mã định danh của thành phố

        Returns:
            list[WeatherStatus]: Danh sách các trạng thái thời tiết của thành phố
        """
        pass
    
    @abstractmethod
    def insert(self, new_weather: WeatherStatus) -> None:
        """
        Thêm một trạng thái thời tiết mới vào CSDL.

        Args:
            new_weather (WeatherStatus): Trạng thái thời tiết mới
        """
        pass
    
    @abstractmethod
    def delete(self, city_id: int, collect_time: datetime) -> None:
        """
        Xóa một trạng thái thời tiết của một thành phố tại 1 thời điểm xác định

        Args:
            city_id (int): Mã định danh của thành phố
            collect_time (datetime): Thời điểm cần xóa
        """
        pass
    
    @abstractmethod
    def delete_all(self, city_id: int) -> None:
        """
        Xóa tất cả các trạng thái thời tiết của một thành phố

        Args:
            city_id (int): Mã định danh của thành phố
        """
        pass
    
class MySQLWeatherStatusDAO(BasicMySQLDAO, BasicWeatherStatusDAO):
    """
    Triển khai các phương thức thao tác với CSDL của các weather status 
    trên CSDL MySQL.
    """
    
    def __init__(self, host, db, user, password):
        """
        Khởi tạo một DAO. Đường dẫn tới Queries file được thêm vào từ `db.info`.
        
        Args:
            host (str): Máy chủ CSDL. Nếu bạn sử dụng localhost (địa chỉ loopback) 
                thì hãy truyền vào giá trị `host='localhost'`.
            db (str): Tên của CSDL.
            user (str): Tên đăng nhập để truy cập vào CSDL, thông thường là `'root'`.
            password (str): Mật khẩu bạn dùng để truy cập CSDL với tên đăng nhập trên.
        """
        super().__init__(host, db, user, password,
                         queriesFile=[dbinfo.GENERAL_WEATHER_SQL_FILE,
                                      dbinfo.WEATHER_STATUS_SQL_FILE,
                                      dbinfo.WEATHER_CONDITION_SQL_FILE])
        self._general_weather_reader = self._sqlFileReaders[dbinfo.GENERAL_WEATHER_SQL_FILE]
        self._weather_status_reader = self._sqlFileReaders[dbinfo.WEATHER_STATUS_SQL_FILE]
        self._weather_condition_reader = self._sqlFileReaders[dbinfo.WEATHER_CONDITION_SQL_FILE]
            
    def get(self, city_id: int, collect_time: datetime) -> WeatherStatus:
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy các query từ 3 bảng liên quan
        get_status_query = self._general_weather_reader.get_query_of(
            dbinfo.GeneralWeatherEnableQueries.GET_BY_STATUS.value
        )      
        get_weather_query = self._weather_status_reader.get_query_of(
            dbinfo.WeatherStatusEnableQueries.GET_BY_CITY_AND_TIME.value
        )
        get_condition_query = self._weather_condition_reader.get_query_of(
            dbinfo.WeatherConditionEnableQueries.GET_ALL_BY_CITY_AND_TIME.value
        )
        
        # Lấy dữ liệu
        try:
            # Lấy từ bảng chính weather_status
            cursor.execute(get_weather_query, (city_id, collect_time))
            get_weather_result = cursor.fetchone()
            if get_weather_result is None:
                raise NotExistDataException()
            
            # Lấy từ bảng weather_condition các mã định danh của kiểu thời tiết chung
            cursor.execute(get_condition_query, (city_id, collect_time))
            conditions: List[tuple] = []
            get_condition_results = cursor.fetchall()
            
            # Lấy chi tiết các kiểu thời tiết chung từ bảng general_weather 
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
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy query từ 3 bảng liên quan
        get_status_query = self._general_weather_reader.get_query_of(
            dbinfo.GeneralWeatherEnableQueries.GET_BY_STATUS.value
        )      
        get_weather_query = self._weather_status_reader.get_query_of(
            dbinfo.WeatherStatusEnableQueries.GET_ALL_BY_CITY.value
        )
        get_condition_query = self._weather_condition_reader.get_query_of(
            dbinfo.WeatherConditionEnableQueries.GET_ALL_BY_CITY_AND_TIME.value
        )
        
        # Lấy dữ liệu
        try:
            # Lấy dữ liệu từ bảng chính weather_status
            cursor.execute(get_weather_query, (city_id, ))
            get_weather_results = cursor.fetchall()
            
            weather_statuses: List[WeatherStatus] = []
            for get_weather_result in get_weather_results:
                # Với mỗi dữ liệu lấy được, lấy mã các kiểu thời tiết từ weather_condition
                collect_time = get_weather_result[1]
                cursor.execute(get_condition_query, (city_id, collect_time))
                conditions: List[tuple] = []
                get_condition_results = cursor.fetchall()
                
                # Lấy chi tiết các kiểu thời tiết từ general_weather
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
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy query để thao tác trên 2 bảng liên quan
        insert_status_query = self._weather_status_reader.get_query_of(
            dbinfo.WeatherStatusEnableQueries.INSERT.value
        )
        insert_condition_query = self._weather_condition_reader.get_query_of(
            dbinfo.WeatherConditionEnableQueries.INSERT.value
        )
        delete_condition_query = self._weather_condition_reader.get_query_of(
            dbinfo.WeatherConditionEnableQueries.DELETE.value
        )
        
        # Thực hiện, nếu có lỗi thì rollback toàn bộ
        try:
            # Thêm trạng thái thời tiết cơ bản vào bảng weather_status
            cursor.execute(insert_status_query, new_weather.to_tuple()[:-1])
            
            # Xóa các condition đã tồn tại tại thành phố ở thời điểm cần thêm (nếu đã có)
            cursor.execute(delete_condition_query, (new_weather.city_id, new_weather.collect_time))
            
            # Với mỗi kiểu thời tiết trong trạng thái mới, thực hiện thêm vào weather_condidtion
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
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy query để xóa (do mối quan hệ khóa ngoài nên không cần xóa ở bảng weather_condition)
        delete_query = self._weather_status_reader.get_query_of(
            dbinfo.WeatherStatusEnableQueries.DELETE.value
        )
        
        # Thực hiện, nếu lỗi thì rollback
        try:
            cursor.execute(delete_query, (city_id, collect_time))
            self._connection.commit()
        except Error as e:
            if self._connection.is_connected():
                self._connection.rollback()
            raise DAOException(e.msg)
        finally:
            cursor.close()
    
    def delete_all(self, city_id: int) -> None:
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy query để xóa (do mối quan hệ khóa ngoài nên không cần xóa ở bảng weather_condition)
        delete_query = self._weather_status_reader.get_query_of(
            dbinfo.WeatherStatusEnableQueries.DELETE_ALL_BY_CITY.value
        )
        
        # Thực hiện, nếu lỗi thì rollback
        try:
            cursor.execute(delete_query, (city_id, ))
            self._connection.commit()
        except Error as e:
            if self._connection.is_connected():
                self._connection.rollback()
            raise DAOException(e.msg)
        finally:
            cursor.close()
            
class MongoDBGeneralWeatherDAO(BasicMongoDBDAO, BasicGeneralWeatherDAO):
    """
    Triển khai các phương thức thao tác với CSDL các general weather
    trên CSDL MongoDB
    """
    
    def __init__(self, host: str, port: int,
                 db: str, user: str|None = None, password: str|None = None):
        """
        Khởi tạo một DAO kết nối tới MongoDB để thao tác dữ liệu general weather

        Args:
            host (str): Máy chủ CSDL, thông thường là `'localhost'`.
            port (int): Cổng phục vụ của MongoDB trên máy chủ, thông thường là `27017`.
            db (str): Cơ sở dữ liệu cần kết nối tới
            user (str | None, optional): Tên đăng nhập, yêu cầu khi CSDL phải xác thực. Defaults to None.
            password (str | None, optional): Mật khẩu, yêu cầu khi CSDL phải xác thực. Defaults to None.
        """ 
        super().__init__(host, port, db, 
                         collection='general_weather',
                         user=user, password=password)
        self._general_weather_collection = self._collections['general_weather']
        
    def get(self, status_id: int) -> GeneralWeather:
        query = {
            'status_id': status_id
        }
        
        result = self._general_weather_collection.find_one(query)
        if result is None:
            raise NotExistDataException()
        return GeneralWeather.from_json(result)
    
    def get_all(self) -> list[GeneralWeather]:
        results = self._general_weather_collection.find()
        general_weathers: List[GeneralWeather] = []
        
        # Với mỗi result thực hiện chuyển đổi
        for result in results:
            general_weathers.append(GeneralWeather.from_json(result))
        return general_weathers

class MongoDBWeatherStatusDAO(BasicMongoDBDAO, BasicWeatherStatusDAO):
    """
    Triển khai các phương thức thao tác với CSDL các weather status
    trên CSDL MongoDB
    """
    
    def __init__(self, host: str, port: int,
                 db: str, user: str|None = None, password: str|None = None):
        """
        Khởi tạo một DAO kết nối tới MongoDB để thao tác dữ liệu weather status

        Args:
            host (str): Máy chủ CSDL, thông thường là `'localhost'`.
            port (int): Cổng phục vụ của MongoDB trên máy chủ, thông thường là `27017`.
            db (str): Cơ sở dữ liệu cần kết nối tới
            user (str | None, optional): Tên đăng nhập, yêu cầu khi CSDL phải xác thực. Defaults to None.
            password (str | None, optional): Mật khẩu, yêu cầu khi CSDL phải xác thực. Defaults to None.
        """ 
        super().__init__(host, port, db, 
                         collection=['general_weather', 'weather_status'],
                         user=user, password=password)
        self._general_weather_collection = self._collections['general_weather']
        self._weather_status_collection = self._collections['weather_status']
        
    def get(self, city_id: int, collect_time: datetime) -> WeatherStatus:
        status_query = {
            '$and': [
                {'city_id': city_id},
                {'collect_time': collect_time}
            ]
        }
        
        # Lấy các status trước
        result = self._weather_status_collection.find_one(status_query)
        if result is None:
            raise NotExistDataException()
        
        # Với mỗi general_weather thì lấy thông tin chi tiết về nó
        general_weathers_dict: List[dict] = []
        for item in result['general_weathers']:
            general_query = {
                'status_id': item['status_id']
            }
            
            general_result = self._general_weather_collection.find_one(general_query)
            general_weathers_dict.append(general_result)
            
        # Tổng hợp
        result['general_weathers'] = general_weathers_dict
        return WeatherStatus.from_json(result)
        
    
    def get_all(self, city_id: int) -> list[WeatherStatus]:
        status_query = {
            'city_id': city_id
        }
        
        # Lấy các status trước
        results = self._weather_status_collection.find(status_query)
        status_results: List[WeatherStatus] = []
        
        # Với mỗi result thì lấy dữ liệu các general weather mà result đó sở hữu
        for result in results:
            # Với mỗi general_weather thì lấy thông tin chi tiết về nó
            general_weathers_dict: List[dict] = []
            for item in result['general_weathers']:
                general_query = {
                    'status_id': item['status_id']
                }
                
                general_result = self._general_weather_collection.find_one(general_query)
                general_weathers_dict.append(general_result)
                
            # Tổng hợp
            result['general_weathers'] = general_weathers_dict
            status_results.append(WeatherStatus.from_json(result))
            
        return status_results
        
    def insert(self, new_weather: WeatherStatus) -> None:
        query = {
            '$and': [
                {'city_id': new_weather.city_id},
                {'collect_time': new_weather.collect_time}
            ]
        }
        
        # Lấy values để update
        values = new_weather.to_json()
        for item in values['general_weathers']:
            item.pop('description')
        update = {
            "$set": values
        }
            
        result = self._weather_status_collection.update_one(query, update, upsert=True)
        if result.upserted_id is None and result.matched_count == 0:
            raise DAOException("Failed inserted!")
    
    def delete(self, city_id: int, collect_time: datetime) -> None:
        query = {
            '$and': [
                {'city_id': city_id},
                {'collect_time': collect_time}
            ]
        }
        
        result = self._weather_status_collection.delete_one(query)
        if result.deleted_count == 0:
            raise DAOException("Failed deleted!")
    
    def delete_all(self, city_id: int) -> None:
        query = {
            'city_id': city_id
        }
        
        result = self._weather_status_collection.delete_many(query)
        if result.deleted_count == 0:
            raise DAOException("Failed deleted!")