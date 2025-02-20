"""
Module `db` lưu giữ các file chứa các hành vi tạo bảng,
khởi tạo dữ liệu và các câu truy vấn. Nó đại diện cho 
tất cả những gì liên quan tới việc cấu hình mô hình 
vật lý cho dữ liệu.

Author: 
    Lê Minh Triết
Last Modified Date: 
    03/02/2025
Module:
    `sql_reader`, `config`
"""

from . import config, sql_reader

__all__ = ['sql_reader', 'config']