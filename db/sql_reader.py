"""
Module `sql_reader` cung cấp đối tượng để có thể đọc và xử lý các file `.sql`
để lấy được các câu lệnh có thể thực hiện.

Module giúp kiểm soát các thao tác có thể gây ảnh hưởng tới CSDL một cách rõ ràng.

Author: 
    Lê Minh Triết
Last Modified Date: 
    23/01/2025
"""

class NotSupportedQueryException(Exception):
    """
    Ngoại lệ được ném ra khi truy vấn không được hỗ trợ.
    """

    def __init__(self, message: str = "This query is not supported!"):
        """
        Hàm khởi tạo của ngoại lệ NotSupportedQueryException.

        Args:
            message (str): Thông điệp của ngoại lệ. Mặc định là "This query is not supported!".
        """
        super().__init__(message)


class SQLFileReader:
    """
    Lớp để đọc và xử lý các câu lệnh SQL từ một file đuôi .sql.
    """

    def __init__(self):
        """
        Hàm khởi tạo của lớp SQLFileReader.
        """
        self._stmts = {}

    def read(self, sql_file_path: str) -> None:
        """
        Đọc các câu lệnh SQL từ một file.
        File SQL bao gồm các câu lệnh truy vấn và thêm/xóa/sửa.
        
        Trước mỗi câu lệnh phải có 1 dòng comment bắt đầu bằng -- và có
        chú thích về loại lệnh phía dưới
        để hàm nhận biết được loại lệnh tương ứng.

        Args:
            sql_file_path (str): Đường dẫn tới file SQL cần đọc.

        Raises:
            Exception: Nếu xảy ra lỗi khi đọc file.
        """
        self.clear()
        
        # Dùng để lưu câu lệnh hiện tại đang duyệt, vì một câu lệnh có thể trên nhiều dòng
        curr_stmt = None 
        sql_commands = []

        try:
            with open(sql_file_path, 'r') as file:
                # Đọc từng dòng trong file
                for line in file:
                    line = line.strip()
                    # Comment chỉ loại câu lệnh
                    if line.startswith("--"):             
                        if curr_stmt is not None and sql_commands:
                            sql_str_commands = ' '.join(sql_commands).strip()
                            self._stmts[curr_stmt] = sql_str_commands
                        curr_stmt = line.replace('--', '').strip()
                        sql_commands = []
                    else:
                        # Nếu không phải comment thì thêm dòng này vào câu lệnh hiện có
                        if line:
                            sql_commands.append(line)
                            
                # Đây là dòng cuối cùng được thêm vào lệnh hiện tại
                if curr_stmt is not None and sql_commands:
                    sql_str_commands = ' '.join(sql_commands).strip()
                    self._stmts[curr_stmt] = sql_str_commands
        except Exception as ioException:
            raise ioException

    def get_enable_queries(self) -> list[str]:
        """
        Lấy danh sách các loại truy vấn có sẵn.

        Returns:
            list: Danh sách các loại truy vấn.
        """
        return list(self._stmts.keys())

    def get_query_of(self, query_type: str) -> str:
        """
        Lấy câu lệnh SQL của loại truy vấn cụ thể.

        Args:
            query_type (str): Loại truy vấn.

        Returns:
            str: Câu lệnh SQL tương ứng với loại truy vấn.

        Raises:
            NotSupportedQueryException: Nếu loại truy vấn không được hỗ trợ.
        """
        if query_type not in self.get_enable_queries():
            raise NotSupportedQueryException()
        return self._stmts[query_type]

    def clear(self) -> None:
        """
        Xóa tất cả các câu lệnh SQL đã lưu trữ.
        """
        self._stmts.clear()