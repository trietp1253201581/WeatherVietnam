"""
Module `dao` cung cấp các DAO để thao tác CSDL
của các country và city

Author: 
    Lê Minh Triết
Last Modified Date: 
    03/02/2025
"""

import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)

from mysql.connector import Error

from typing import List
from abc import ABC, abstractmethod

import db.config as dbconfig
from common.dao import BasicMySQLDAO, DAOException, NotExistDataException, BasicMongoDBDAO

from place.model import Country, City

class BasicCountryDAO(ABC):
    """
    Cung cấp các phương thức có thể thao tác trên CSDL các country.
    Các class phải thực thi các phương thức trừu tượng này.
    """
    
    @abstractmethod
    def get(self, code: str) -> Country:
        """
        Lấy 1 country theo mã có sẵn. Code của country được nhập vào phải theo
        chuẩn ISO 3166-1, có thể theo 2 dạng Alpha-2 hoặc Alpha-3.
        
        Args:
            code (str): Mã quốc gia theo ISO 3166-1(Alpha-2/Alpha-3)

        Returns:
            Country: Đối tượng Country thu được (khi không tồn tại sẽ ném ra exception).
        """
        pass
    
    @abstractmethod
    def insert(self, new_country: Country) -> None:
        """
        Thêm một Country vào CSDL.
        
        Args:
            new_country (Country): Country được thêm vào.
        """
        pass
    
    @abstractmethod
    def delete(self, code: str) -> None:
        """
        Xóa một country có mã xác định trong CSDL.
        Args:
            code (str): Mã của country cần xóa.
        """
        pass

class MySQLCountryDAO(BasicMySQLDAO, BasicCountryDAO):
    """
    Triển khai các phương thức thao tác với CSDL của các country 
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
                         queriesFile=dbconfig.COUNTRY_SQL_FILE)
        self._country_reader = self._sqlFileReaders[dbconfig.COUNTRY_SQL_FILE]
    
    def get(self, code: str) -> Country:
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy các query tương ứng
        get_country_query = self._country_reader.get_query_of(
            dbconfig.CountryEnableQueries.GET_BY_CODE.value
        )
        
        # Thực hiển đổi code về dạng ISO 3166-1 Alpha-2
        country = Country(code)
        code = country.code
        
        # Execute truy vấn và lấy kết quả
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
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy query tương ứng
        insert_country_query = self._country_reader.get_query_of(
            dbconfig.CountryEnableQueries.INSERT.value
        )
        
        # Thực hiện lệnh, nếu có lỗi thì sẽ rollback lại
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
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")       
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy query
        delete_query = self._country_reader.get_query_of(
            dbconfig.CountryEnableQueries.DELETE.value
        )
        
        # Đổi code sang ISO 3166-1 Alpha-2
        country = Country(code)
        code = country.code
        
        # Thực hiện lệnh, nếu có lỗi thì rollback
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
    """
    Cung cấp các phương thức có thể thao tác trên CSDL các city.
    Các class phải thực thi các phương thức trừu tượng này.
    """
    
    @abstractmethod
    def get(self, city_id: int|None = None, city_name: str|None = None) -> City:
        """
        Lấy dữ liệu của một City trong CSDL. Tham số dùng để lấy dữ liệu có thể là
        id của thành phố (khuyên dùng, nếu không chắc có thể dùng phương thức `get_all(country_code)`)
        để biết id của các thành phố, hoặc là tên của thành phố (có thể khác tên bạn biết)

        Args:
            city_id (int | None, optional): Id của thành phố. Defaults to None.
            city_name (str | None, optional): Tên của thành phố, chỉ được sử dụng nếu
                `city_id=None`. Defaults to None.

        Returns:
            City: Đối tượng City thu được (nếu không tồn tại sẽ ném ra ngoại lệ)
        """
        pass
    
    @abstractmethod
    def insert(self, new_city: City) -> None:
        """
        Thêm 1 City vào CSDL.
        
        Args:
            new_city (City): City cần được thêm vào
        """
        pass
    
    @abstractmethod
    def delete(self, city_id: int) -> None:
        """
        Xóa một city có id xác định trong CSDL
        Args:
            city_id (int): Id của city cần xóa.
        """
        pass
    
    @abstractmethod
    def get_all(self, country_code: str) -> list[City]:
        """
        Lấy tất cả các thành phố của 1 quốc gia.
        
        Args:
            country_code (str): Mã quốc gia chứa các thành phố cần lấy

        Returns:
            list[City]: Danh sách các thành phố của quốc gia đó (nếu không
                có thành phố nào sẽ trả về danh sách trống)
        """
        pass

class MySQLCityDAO(BasicMySQLDAO, BasicCityDAO):
    """
    Triển khai các phương thức thao tác với CSDL các city
    trên CSDL MySQL
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
                         queriesFile=[dbconfig.COUNTRY_SQL_FILE,
                                      dbconfig.CITY_SQL_FILE])
        self._country_reader = self._sqlFileReaders[dbconfig.COUNTRY_SQL_FILE]
        self._city_reader = self._sqlFileReaders[dbconfig.CITY_SQL_FILE]
        
    def get(self, city_id: int|None = None, city_name: str|None = None) -> City:
        if city_id is None and city_name is None:
            raise NotExistDataException()
        
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy các query tương ứng (có cả thao tác với country)
        get_country_query = self._country_reader.get_query_of(
            dbconfig.CountryEnableQueries.GET_BY_CODE.value
        )
        get_city_query = self._city_reader.get_query_of(
            dbconfig.CityEnableQueries.GET_BY_ID.value
        )
        get_city_name_query = self._city_reader.get_query_of(
            dbconfig.CityEnableQueries.GET_BY_NAME.value
        )

        # Lấy dữ liệu, tùy thuộc vào có city_id hay không để quyết định chọn query nào
        try:
            if city_id is not None:
                cursor.execute(get_city_query, (city_id, ))
                get_city_result = cursor.fetchone()
            else:
                cursor.execute(get_city_name_query, (city_name, ))
                get_city_result = cursor.fetchone()
            if get_city_result is None:
                raise NotExistDataException()
            
            # Lấy dữ liệu quốc gia mà thành phố thuộc về
            country_source = None
            country_code = get_city_result[5]
            if country_code is not None:
                cursor.execute(get_country_query, (country_code, ))
                get_country_result = cursor.fetchone()
                country_source = get_country_result
                
            source = get_city_result[:-1] + (country_source, )
            return City.from_tuple(source)
        except Error as e:
            raise DAOException(e.msg)
        finally:
            cursor.close()
            
    def insert(self, new_city: City) -> None:
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy các query
        insert_country_query = self._country_reader.get_query_of(
            dbconfig.CountryEnableQueries.INSERT.value
        )
        insert_city_query = self._city_reader.get_query_of(
            dbconfig.CityEnableQueries.INSERT.value
        )
        
        # Thêm vào CSDL, nếu lỗi thì rollback. Nếu quốc gia mà city thuộc về chưa có thì cũng thêm.
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
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy query
        delete_query = self._city_reader.get_query_of(
            dbconfig.CityEnableQueries.DELETE.value
        )
        
        # Thực hiện xóa, nếu lỗi thì rollback
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
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy các query
        get_country_query = self._country_reader.get_query_of(
            dbconfig.CountryEnableQueries.GET_BY_CODE.value
        )
        get_city_query = self._city_reader.get_query_of(
            dbconfig.CityEnableQueries.GET_ALL_BY_COUNTRY.value
        )

        # Lấy dữ liệu từ bảng country và city
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
            
class MongoDBCountryDAO(BasicMongoDBDAO, BasicCountryDAO):
    """
    Triển khai các phương thức thao tác với CSDL các city
    trên CSDL MongoDB
    """
    
    def __init__(self, host: str, port: int,
                 db: str, user: str|None = None, password: str|None = None):
        """
        Khởi tạo một DAO kết nối tới MongoDB để thao tác dữ liệu country

        Args:
            host (str): Máy chủ CSDL, thông thường là `'localhost'`.
            port (int): Cổng phục vụ của MongoDB trên máy chủ, thông thường là `27017`.
            db (str): Cơ sở dữ liệu cần kết nối tới
            user (str | None, optional): Tên đăng nhập, yêu cầu khi CSDL phải xác thực. Defaults to None.
            password (str | None, optional): Mật khẩu, yêu cầu khi CSDL phải xác thực. Defaults to None.
        """ 
        super().__init__(host, port, db, 
                         collection='country',
                         user=user, password=password)
        self._country_collection = self._collections['country']
    
    def get(self, code: str) -> Country:
        query = {
            'code': Country(code).code
        }
        
        result = self._country_collection.find_one(query)
        if result is None:
            raise NotExistDataException()
        return Country.from_json(source=result)
    
    def insert(self, new_country: Country) -> None:
        query = {
            'code': new_country.code
        }
        update = {
            '$set': new_country.to_json()
        }
        
        result = self._country_collection.update_one(query, update, upsert=True)
        if result.upserted_id is None and result.matched_count == 0:
            raise DAOException("Failed insert")
    
    def delete(self, code: str) -> None:
        query = {
            'code': code
        }
        
        result = self._country_collection.delete_one(query)
        if result.deleted_count == 0:
            raise DAOException("Failed deleted!")
        
class MongoDBCityDAO(BasicMongoDBDAO, BasicCityDAO):
    """
    Triển khai các phương thức thao tác với CSDL các city
    trên CSDL MongoDB
    """
    
    def __init__(self, host: str, port: int,
                 db: str, user: str|None = None, password: str|None = None):
        """
        Khởi tạo một DAO kết nối tới MongoDB để thao tác dữ liệu city

        Args:
            host (str): Máy chủ CSDL, thông thường là `'localhost'`.
            port (int): Cổng phục vụ của MongoDB trên máy chủ, thông thường là `27017`.
            db (str): Cơ sở dữ liệu cần kết nối tới
            user (str | None, optional): Tên đăng nhập, yêu cầu khi CSDL phải xác thực. Defaults to None.
            password (str | None, optional): Mật khẩu, yêu cầu khi CSDL phải xác thực. Defaults to None.
        """ 
        super().__init__(host, port, db, 
                         collection=['country', 'city'],
                         user=user, password=password)
        self._country_collection = self._collections['country']
        self._city_collection = self._collections['city']
    
    def get(self, city_id: str|None = None, city_name: str|None = None) -> City:
        if city_id is None and city_name is None:
            raise NotExistDataException()
        if city_id is not None:
            city_query = {
                'city_id': city_id
            }
        else:
            city_query = {
                'name': city_name
            }
        
        # Lấy city
        city_result = self._city_collection.find_one(city_query)
        if city_result is None:
            raise NotExistDataException()
        
        # Lấy thông tin country mà city thuộc về
        country_query = {
            'code': city_result['country']['code']
        }
        country_result = self._country_collection.find_one(country_query)
        
        # Tổng hợp
        city_result['country'] = country_result
        return City.from_json(city_result)
    
    def insert(self, new_city: City) -> None:
        # Lấy các query và values
        city_query = {
            'city_id': new_city.city_id
        }
        values = new_city.to_json()
        values['country'].pop('name')
        city_update = {
            '$set': values
        }
        country_query = {
            'code': new_city.country.code
        }
        country_update = {
            '$set': new_city.country.to_json()
        }
        
        # Thêm country nếu cần trước
        country_result = self._country_collection.update_one(country_query, country_update, upsert=True)
        if country_result.upserted_id is None and country_result.matched_count == 0:
            raise Exception("Failed insert country!")

        # Thêm city
        city_result = self._city_collection.update_one(city_query, city_update, upsert=True)
        if city_result.upserted_id is None and city_result.matched_count == 0:
            raise Exception("Failed insert city!")
        
    def delete(self, city_id: int) -> None:
        query = {
            'city_id': city_id
        }
        
        result = self._city_collection.delete_one(query)
        if result.deleted_count == 0:
            raise DAOException("Failed deleted!")
    
    def get_all(self, country_code):
        city_query = {
            'country.code': country_code
        }
        
        # Lấy danh sách các city result
        city_results = self._city_collection.find(city_query)
        results: List[City] = []
        for city_result in city_results:
            # Với mỗi city thì lấy thông tin country
            # Lấy thông tin country mà city thuộc về
            country_query = {
                'code': city_result['country']['code']
            }
            country_result = self._country_collection.find_one(country_query)
            
            # Tổng hợp
            city_result['country'] = country_result
            results.append(City.from_json(city_result))
        
        return results