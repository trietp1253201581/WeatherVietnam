"""
Module `dao` cung cấp những thao tác cơ bản, chung nhất
mà mọi Data Access Object (DAO) cần phải có.

Author: 
    Lê Minh Triết
Last Modified Date: 
    02/02/2025
"""

# Cấu hình đường dẫn tới thư mục ban đầu
import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)

from typing import Dict

import mysql.connector
from mysql.connector import Error

from db.sql_reader import SQLFileReader

class DAOException(Exception):
    """
    Đại diện cho các ngoại lệ có thể xảy ra khi thao tác với một DAO.
    """
    
    def __init__(self, message: str):
        """
        Khởi tạo một ngoại lệ có thể xảy ra khi thao tác với một DAO.
        
        Args:
            message (str): Thông điệp lưu giữ thông tin về lỗi/ngoại lệ xảy ra
        """
        super().__init__(message)
        
class NotExistDataException(DAOException):
    """
    Ngoại lệ được ném ra khi không tìm được dữ liệu.
    """
    
    def __init__(self, message: str = "Not found!"):
        """
        Khởi tạo một ngoại lệ có thể xảy ra khi không tìm được dữ liệu.
        
        Args:
            message (str): Thông điệp lưu giữ thông tin về lỗi/ngoại lệ xảy ra,
            mặc định là `'Not found!'`
        """
        super().__init__(message)
        
class BasicMySQLDAO:
    """
    Cung cấp các phương thức cơ bản mà một DAO với CSDL MySQL cần phải có.
    Đó là các phương thức để kết nối tới CSDL và phương thức để đọc các 
    câu lệnh cho phép từ một file sql.
    """
    
    def __init__(self, host: str, db: str, user: str, password: str, queriesFile: str|list[str]|None = None):
        """
        Khởi tạo một DAO chung cho các DAO dùng CSDL MySQL.
        
        Args:
            host (str): Máy chủ CSDL. Nếu bạn sử dụng localhost (địa chỉ loopback) 
                thì hãy truyền vào giá trị `host='localhost'`.
            db (str): Tên của CSDL.
            user (str): Tên đăng nhập để truy cập vào CSDL, thông thường là `'root'`.
            password (str): Mật khẩu bạn dùng để truy cập CSDL với tên đăng nhập trên.
            queriesFile (str | list[str] | None, optional): Đường dẫn tới các file
                sql cần đọc, có thể có nhiều đường dẫn tới nhiều file. Defaults to None.
        """
        self.connect_(host, db, user, password)
        self._sqlFileReaders: Dict[str, SQLFileReader] = {}
        self.get_sql_file_reader_(queriesFile)
        
    def connect_(self, host: str, db: str, user: str, password: str):
        """
        Thiết lập kết nối tới CSDL với các thông tin được truyền vào.
        
        Args:
            host (str): Máy chủ CSDL. Nếu bạn sử dụng localhost (địa chỉ loopback) 
                thì hãy truyền vào giá trị `host='localhost'`.
            db (str): Tên của CSDL.
            user (str): Tên đăng nhập để truy cập vào CSDL, thông thường là `'root'`.
            password (str): Mật khẩu bạn dùng để truy cập CSDL với tên đăng nhập trên.

        Raises:
            DAOException: Nếu như kết nối không thành công, có thể dẫn tới do truyền vào
            tham số nào đó sai, hoặc CSDL từ chối kết nối của bạn.
        """
        try:
            self._connection = mysql.connector.connect(
                host=host,
                database=db,
                user=user,
                password=password
            )              
        except Error as ex:
            raise DAOException(ex.msg)
        
    def get_sql_file_reader_(self, queriesFile: str|list[str]|None):
        """
        Đọc các file sql và lấy những câu lệnh hợp lệ từ file đó.
        
        Các câu lệnh sẽ được lưu vào 1 dict (attribute của class), với
        key là định danh của file (đường dẫn tới file đó) và value là
        list các câu lệnh hợp lệ được đọc từ file đó.
        
        Có thể xem thêm module `db.info`.
        
        Args:
            queriesFile (str | list[str] | None): Đường dẫn tới các file
                sql cần đọc, có thể có nhiều đường dẫn tới nhiều file.

        Raises:
            DAOException: Nếu việc đọc bất cứ 1 file nào bị lỗi.
        """
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
                raise DAOException(f"Can't read {file}!")
                
    def close_connection(self):
        """
        Đóng lại kết nối tới CSDL hiện tại.
        """
        self._connection.close()
