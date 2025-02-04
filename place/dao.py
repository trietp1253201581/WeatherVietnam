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

import db.info as dbinfo
from common.dao import BasicMySQLDAO, DAOException, NotExistDataException

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
                         queriesFile=dbinfo.COUNTRY_SQL_FILE)
        self._country_reader = self._sqlFileReaders[dbinfo.COUNTRY_SQL_FILE]
    
    def get(self, code: str) -> Country:
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy các query tương ứng
        get_country_query = self._country_reader.get_query_of(
            dbinfo.CountryEnableQueries.GET_BY_CODE.value
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
            dbinfo.CountryEnableQueries.INSERT.value
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
            dbinfo.CountryEnableQueries.DELETE.value
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
                         queriesFile=[dbinfo.COUNTRY_SQL_FILE,
                                      dbinfo.CITY_SQL_FILE])
        self._country_reader = self._sqlFileReaders[dbinfo.COUNTRY_SQL_FILE]
        self._city_reader = self._sqlFileReaders[dbinfo.CITY_SQL_FILE]
        
    def get(self, city_id: int|None = None, city_name: str|None = None) -> City:
        if city_id is None and city_name is None:
            raise NotExistDataException()
        
        # Check kết nối và lấy cursor
        if not self._connection.is_connected():
            raise DAOException("Connection is null!")
        cursor = self._connection.cursor(prepared=True)
        
        # Lấy các query tương ứng (có cả thao tác với country)
        get_country_query = self._country_reader.get_query_of(
            dbinfo.CountryEnableQueries.GET_BY_CODE.value
        )
        get_city_query = self._city_reader.get_query_of(
            dbinfo.CityEnableQueries.GET_BY_ID.value
        )
        get_city_name_query = self._city_reader.get_query_of(
            dbinfo.CityEnableQueries.GET_BY_NAME.value
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
            dbinfo.CountryEnableQueries.INSERT.value
        )
        insert_city_query = self._city_reader.get_query_of(
            dbinfo.CityEnableQueries.INSERT.value
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
            dbinfo.CityEnableQueries.DELETE.value
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
            dbinfo.CountryEnableQueries.GET_BY_CODE.value
        )
        get_city_query = self._city_reader.get_query_of(
            dbinfo.CityEnableQueries.GET_ALL_BY_COUNTRY.value
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