"""
Module `business` cung cấp các nghiệp vụ với
các country và city

Author: 
    Lê Minh Triết
Last Modified Date: 
    03/02/2025
"""

import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)

import json
import requests

from typing import Literal, Dict, List

from place.model import City, Country
from place.dao import BasicCityDAO, BasicCountryDAO

def extract_from_open_weather(city: City) -> tuple[float, float]:
    """
    Lấy tọa độ của 1 City từ API địa lý của Open Weather Map. API đã có trong file
    `README.md`. API Key được lưu trong file config.json (được ẩn đi để bảo mật)

    Args:
        city (City): Thành phố cần lấy tọa độ. Các thuộc tính được sử dụng là tên 
            của thành phố và code của country mà thành phố thuộc về.

    Returns:
        tuple[float, float]: Tọa độ (lon, lat) (kinh độ, vĩ độ) của thành phố
    """
    # Mở file cấu hình và lấy API Key
    config_dir = os.path.join(init_dir, 'config.json')
    with open(config_dir, 'r') as config_file:
        config = json.load(config_file)
    api_key = config['OPEN_WEATHER_MAP_API_KEY']
    
    # Lấy dữ liệu từ API
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    url = f"{base_url}?q={city.name},{city.country.code}&limit=1&appid={api_key}"
    response = requests.get(url).json()[0]
    return response['lon'], response['lat']

def _get_city(city: int|str,
              city_dao: BasicCityDAO) -> City:
    """
    Lấy 1 đối tượng city đơn lẻ từ CSDL. Nếu đối tượng này chưa có tọa độ địa lý
    thì sẽ tự động gọi tới hàm `extract_from_open_weather` để lấy dữ liệu từ API
    và thêm vào CSDL.

    Args:
        city (int | str): Id hoặc name của thành phố, khuyên dùng Id.
        city_dao (BasicCityDAO): Một DAO có thể thao tác trên CSDL các city.

    Returns:
        City: City lấy được (có thể được thêm tọa độ địa lý)
    """
    if isinstance(city, int):
        result_city = city_dao.get(city_id=city)
    else:
        result_city = city_dao.get(city_name=city)
    if result_city.lon is None or result_city.lat is None:
        result_city.lon, result_city.lat = extract_from_open_weather(result_city)
        city_dao.insert(result_city)
    return result_city

def _get_all_of_country(country: str,
                        city_dao: BasicCityDAO) -> list[City]:
    """
    Lấy tất cả các city của một country. Nếu đối tượng city nào đó chưa có tọa độ địa lý
    thì sẽ tự động gọi tới hàm `extract_from_open_weather` để lấy dữ liệu từ API
    và thêm vào CSDL.

    Args:
        country (str): code của country cần lấy
        city_dao (BasicCityDAO): Một DAO có thể thao tác được trên CSDL các city.

    Returns:
        list[City]: Danh sách các thành phố có tọa độ địa lý đầy đủ
    """
    citys = city_dao.get_all(country_code=country)
    for result_city in citys:
        if result_city.lon is None or result_city.lat is None:
            result_city.lon, result_city.lat = extract_from_open_weather(result_city)
            city_dao.insert(result_city)
    return citys

def get_city(city_dao: BasicCityDAO, 
             type: Literal['list_country', 'all_country', 'one_city'] = 'one_city',
             city: int|str|None = None,
             country: str|list[str]|None = None):
    """
    Lấy thông tin của các thành phố theo một quy cách nào đó.

    Args:
        city_dao (BasicCityDAO): Một DAO có thể thao tác trên CSDL các city.
        type (Literal[&#39;list_country&#39;, &#39;all_country&#39;, &#39;one_city&#39;], optional): Quy cách lấy các thành phố.
            `'one_city'`: Lấy 1 thành phố đơn, lúc này sẽ dùng tới tham số `city`.
            `'all_country'`: Lấy các thành phố của 1 quốc gia, sẽ dùng tới tham số `country`.
            `'list_country'`: Lấy các thành phố của nhiều quốc gia, sẽ dùng tới tham số `country`.
            Defaults to 'one_city'.
        city (int | str | None, optional): Định danh cho thành phố cần lấy (id hoặc name). Defaults to None.
        country (str | list[str] | None, optional): Danh sách mã các quốc gia cần lấy. Defaults to None.

    Returns:
        _type_: Tùy thuộc vào quy cách lấy, có thể là một City, 1 list các City, một dict lưu giữ
        các list City của một Country, hoặc là None.
    """
    
    if type == 'one_city' and city is not None:
        return _get_city(city, city_dao)
    elif type == 'all_country' and isinstance(country, str):
        return _get_all_of_country(country, city_dao)
    elif type == 'list_country' and isinstance(country, list):
        results_city_dict: Dict[str, list[City]] = {}
        for one_country in country:
            results_city_dict[one_country] = _get_all_of_country(country)
        return results_city_dict
    else:
        return None
    
def insert_city(city_dao: BasicCityDAO,
                new_city: City|list[City]) -> None:
    """
    Thêm 1 hoặc nhiều City vào CSDL

    Args:
        city_dao (BasicCityDAO): Một DAO có thể thao tác trên CSDL các city.
        new_city (City | list[City]): 1 hoặc nhiều thành phố mới cần thêm.
    """
    if isinstance(new_city, City):
        new_citys = [new_city]
    else:
        new_citys = new_city

    for city in new_citys:
        city_dao.insert(city)
        
def delete_city(city_dao: BasicCityDAO,
                city: City|int|list[City|int]) -> None:
    """
    Xóa 1 hoặc nhiều thành phố trong CSDL. 

    Args:
        city_dao (BasicCityDAO): Một DAO có thể thao tác trên CSDL các city.
        city (City | int | list[City | int]): Một hoặc nhiều City cần xóa. Mỗi City có
            thể được biểu diễn dưới dạng 1 đối tượng hoặc id của City cần xóa.
    """
    if isinstance(city, City):
        city_ids = [city.city_id]
    elif isinstance(city, int):
        city_ids = [city]
    else:
        city_ids: List[int] = []
        for city_item in city:
            if isinstance(city_item, City):
                city_ids.append(city_item.city_id)
            else:
                city_ids.append(city_item)
    
    for city_id in city_ids:
        city_dao.delete(city_id) 
        
def get_country(country_code: str,
                country_dao: BasicCountryDAO) -> Country:
    """
    Lấy Country theo code.

    Args:
        country_code (str): Code của country theo ISO 3166-1 (Alpha-2/Alpha-3).
        country_dao (BasicCountryDAO): Một DAO có thể thao tác trên CSDL các country.

    Returns:
        Country: Đối tượng Country được trả về
    """
    return country_dao.get(country_code)