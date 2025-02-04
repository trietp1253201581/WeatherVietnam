"""
Module `model` cung cấp class để đại diện
cho các đối tượng dữ liệu liên quan tới vị trí,
đó là Country và City.

Author: 
    Lê Minh Triết
Last Modified Date: 
    03/02/2025
"""

import pycountry
from typing import Literal

class Country:
    """
    Đại diện cho 1 đối tượng dữ liệu country.
    """
    
    def __init__(self, code: str, name: str|None = None):
        """
        Khởi tạo 1 đối tượng Country.
        
        Args:
            code (str): Mã của quốc gia theo chuẩn ISO 3166-1, có thể theo Alpha-2 
                hoặc Alpha-3, tuy nhiên khi khởi tạo sẽ chỉ lưu dưới dạng Alpha-2 
            name (str | None, optional): Tên của quốc gia. Defaults to None.
        """
        self.code = code
        self.name = name
        
    @property
    def code(self):
        return self.__code
    
    @property
    def name(self):
        return self.__name
    
    @code.setter
    def code(self, code: str):
        # Dùng module pycountry để lấy đối tượng Country theo ISO 
        # tùy thuộc vào code là Alpha-2 hay Alpha-3, sau đó đều
        # chuyển về Alpha-2
        try:
            if len(code) == 2:
                country_iso = pycountry.countries.get(alpha_2=code.upper())
            elif len(code) == 3:
                country_iso = pycountry.countries.get(alpha_3=code.upper())
            else:
                raise ValueError("Invalid country code!")
            self.__code = country_iso.alpha_2
        except ValueError as valueErr:
            raise ValueError("Invalid country code!")
        
    @name.setter
    def name(self, name: str|None):
        self.__name = name
            
    def get_code_with_type(self, code_type: Literal['alpha_2', 'alpha_3'] = 'alpha_3') -> str:
        """
        Lấy mã quốc gia theo loại Alpha-2 hoặc Alpha-3
        
        Args:
            code_type (Literal[&#39;alpha_2&#39;, &#39;alpha_3&#39;]): Loại mã cần lấy.
                Defaults to `'alpha_3'`.

        Raises:
            ValueError: Xảy ra khi có lỗi, có thể do mã quốc gia bị sai.

        Returns:
            str: Mã quốc gia theo loại tương ứng
        """
        if self.__code is None:
            raise ValueError("Code is null!")
        try:
            country_iso = pycountry.countries.get(alpha_2=self.code)
            if code_type == 'alpha_2':
                return country_iso.alpha_2
            else:
                return country_iso.alpha_3
        except ValueError as e:
            raise e
        
    def get_iso_name(self) -> str:
        """
        Trả về tên của quốc gia này theo chuẩn ISO.
        
        Raises:
            ValueError: Xảy ra khi có lỗi, có thể do mã quốc gia bị sai.

        Returns:
            str: Tên của quốc gia theo chuẩn ISO
        """
        try:
            country_iso = pycountry.countries.get(alpha_2=self.__code)
            return country_iso.name
        except ValueError as e:
            raise e
        
    def get_offical_name(self) -> str:
        """
        Trả về tên chính thức của quốc gia này theo chuẩn ISO.
        
        Raises:
            ValueError: Xảy ra khi có lỗi, có thể do mã quốc gia bị sai.

        Returns:
            str: Tên chính thức của quốc gia theo chuẩn ISO
        """
        try:
            country_iso = pycountry.countries.get(alpha_2=self.__code)
            return country_iso.official_name
        except ValueError as e:
            raise e
        
    def __str__(self):
        s = f'Country('
        s += f'code={self.__code}, '
        s += f'name={self.__name}'
        s += f')'
        return s
    
    @staticmethod
    def from_tuple(source: tuple[str, str|None]) -> 'Country':
        """
        Chuyển đổi 1 tuple sang một đối tượng Country.
        
        Args:
            source (tuple[str, str | None]): dữ liệu nguồn cho dưới dạng 1 tuple,
                với thứ tự các thành phần là code và name của country

        Raises:
            ValueError: Khi source không có đủ 2 thành phần.

        Returns:
            Country: Đối tượng Country thu được
        """
        if len(source) == 0:
            return None
        if len(source) != 2:
            raise ValueError("Invalid argurment, required 2 argument!")
        return Country(
            code=source[0],
            name=source[1]
        )
    
    def to_tuple(self) -> tuple[str, str|None]:
        """
        Chuyển đổi đối tượng này thành 1 tuple theo thứ tự (code, name).

        Returns:
            tuple[str, str|None]: tuple thu được có dạng (code, name).
        """
        return self.__code, self.__name
    
class City:
    """
    Đối tượng đại diện cho dữ liệu của các City.
    """
    def __init__(self, city_id: int, 
                 name: str|None = None,
                 lon: float = 0.0,
                 lat: float = 0.0,       
                 time_zone: int = 0,
                 country: Country|None = None):
        """
        Khởi tạo 1 đối tượng City.

        Args:
            city_id (int): Mã định danh của thành phố (lấy theo CCCD), xem ở `db/db_info.md`.
            name (str | None, optional): Tên của thành phố. Defaults to None.
            lon (float, optional): Kinh độ của thành phố. Defaults to 0.0.
            lat (float, optional): Vĩ độ của thành phố. Defaults to 0.0.
            time_zone (int, optional): Múi giờ của thành phố (phải nằm trong [-12, 14]). 
                Defaults to 0.
            country (Country | None, optional): Quốc gia mà thành phố thuộc về. Defaults to None.
        """
        self.city_id = city_id
        self.name = name
        self.lat = lat
        self.lon = lon
        self.time_zone = time_zone
        self.country = country
    
    @property
    def city_id(self):
        return self.__city_id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def lat(self):
        return self.__lat
    
    @property
    def lon(self):
        return self.__lon
    
    @property
    def time_zone(self):
        return self.__time_zone
    
    @property
    def country(self):
        return self.__country
    
    @city_id.setter
    def city_id(self, city_id: int):
        self.__city_id = city_id
        
    @name.setter
    def name(self, name: str|None):
        self.__name = name
    
    @lat.setter
    def lat(self, lat: float):
        self.__lat = lat
    
    @lon.setter
    def lon(self, lon: float):
        self.__lon = lon
    
    @time_zone.setter
    def time_zone(self, time_zone: int):
        if time_zone < -12 or time_zone > 14:
            raise ValueError("Time zone not in UTC-12 to UTC+14!")
        self.__time_zone = time_zone
    
    @country.setter
    def country(self, country: Country|None):
        self.__country = country
        
    def get_coord(self) -> tuple[float, float]:
        return self.__lon, self.__lat
    
    def __str__(self):
        s = f'City('
        s += f'city_id={self.city_id}, '
        s += f'name={self.name}, '
        s += f'lon={self.lon:.2f}, ' if self.lon is not None else 'lon=None, '
        s += f'lat={self.lat:.2f}, ' if self.lat is not None else 'lat=None, '
        s += f'time_zone=UTC{"+" if self.time_zone>=0 else "-"}{abs(self.time_zone)}, '
        s += f'country={self.country}'
        s += f')'
        return s
    
    @staticmethod
    def from_tuple(source: tuple[int, str|None, float, float, int, tuple]) -> 'City':
        """
        Chuyển đổi 1 tuple sang một đối tượng City.

        Args:
            source (tuple[int, str | None, float, float, int, tuple]): Một tuple
                có dạng (city_id, name, lon, lat, time_zone, country).

        Raises:
            ValueError: Khi tuple không có đủ 6 tham số

        Returns:
            City: Đối tượng City tương ứng
        """
        if len(source) == 0:
            return None
        if len(source) != 6:
            raise ValueError("Invalid argurment, required 6 argument!")
        return City(
            city_id=source[0],
            name=source[1],
            lon=source[2],
            lat=source[3],
            time_zone=source[4],
            country=Country.from_tuple(source[5])
        )
        
    def to_tuple(self) -> tuple[int, str|None, float, float, int, tuple]:
        """
        Chuyển 1 đối tượng City sang một tuple

        Returns:
            tuple[int, str|None, float, float, int, tuple]: tuple tương ứng với thứ tự
                (city_id, name, lon, lat, time_zone, country)
        """
        return self.__city_id, self.__name, self.__lon, self.__lat, self.__time_zone, self.__country.to_tuple()