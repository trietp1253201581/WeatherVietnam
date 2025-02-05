"""
Module `business` cung cấp các nghiệp vụ với
các trạng thái và kiểu thời tiết

Author: 
    Lê Minh Triết
Last Modified Date: 
    04/02/2025
"""

import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)

from typing import List
from datetime import datetime

from weather.model import WeatherStatus, GeneralWeather
from weather.dao import BasicGeneralWeatherDAO, BasicWeatherStatusDAO

import requests
import json

def extract_from_open_weather(lon: float, lat: float) -> dict:
    """
    Extract dữ liệu thời tiết từ API của Open Weathep Map.
    Sẽ sử dụng 2 API, một API về Current Weather, một API
    về Air Pollution.

    Args:
        lon (float): Kinh độ của thành phố
        lat (float): Vĩ độ của thành phố

    Returns:
        dict: Một dict có 2 key là `weather` và `air`, lưu giữ lần lượt
        các response của 2 API kể trên
    """
    # Mở file cấu hình và lấy API Key
    config_dir = os.path.join(init_dir, 'config.json')
    with open(config_dir, 'r') as config_file:
        config = json.load(config_file)
    api_key = config['OPEN_WEATHER_MAP_API_KEY']
    
    # Set tham số cho request
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key
    }
    
    # Thực hiện lấy dữ liệu Current Weather
    weather_base_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_response = requests.get(weather_base_url, params=params).json()
    
    # Thực hiện lấy dữ liệu Air Pollution
    air_base_url = "https://api.openweathermap.org/data/2.5/air_pollution"
    air_response = requests.get(air_base_url, params=params).json()
    
    # Tổng hợp kết quả
    response = {
        'weather': weather_response,
        'air': air_response
    }
    return response

def transform(json_data: dict, city_id: int) -> WeatherStatus:
    """
    Chuyển đổi response dạng JSON về model có thể thao tác với CSDL

    Args:
        json_data (dict): Response thu được từ API, có dạng JSON
        city_id (int): Mã định danh của thành phố mà tại đó thu thập dữ liệu này

    Returns:
        WeatherStatus: Đối tượng model đại diện cho trạng thái thời tiết của thành phố
    """
    # Lấy từng thành phần
    weather_data = json_data['weather']
    air_data = json_data['air']
    
    # Lấy riêng các trạng thái thời tiết
    general_weathers: List[GeneralWeather] = []
    for item in weather_data['weather']:
        general_weathers.append(GeneralWeather(status_id=item['id']))
    
    # Ánh xạ mỗi trường trong response tới các thuộc tính của model
    return WeatherStatus(
        city_id=city_id,
        collect_time=datetime.fromtimestamp(weather_data['dt']),
        temp=weather_data['main']['temp'],
        feels_temp=weather_data['main']['feels_like'],
        pressure=weather_data['main']['pressure'],
        humidity=weather_data['main']['humidity'],
        sea_level=weather_data['main']['sea_level'],
        grnd_level=weather_data['main']['grnd_level'],
        visibility=weather_data['visibility'],
        wind_speed=weather_data['wind']['speed'],
        wind_deg=weather_data['wind']['deg'],
        wind_gust=weather_data['wind']['gust'] if 'gust' in weather_data['wind'] else 0,
        clouds_all=weather_data['clouds']['all'],
        rain=weather_data['rain']['1h'] if 'rain' in weather_data else None,
        sunrise=datetime.fromtimestamp(weather_data['sys']['sunrise']),
        sunset=datetime.fromtimestamp(weather_data['sys']['sunset']),
        aqi=air_data['list'][0]['main']['aqi'],
        pm2_5=air_data['list'][0]['components']['pm2_5'],
        general_weathers=general_weathers
    )
    
def load(weather_status_dao: BasicWeatherStatusDAO,
         new_weather_status: WeatherStatus) -> None:
    """
    Load dữ liệu về trạng thái thời tiết vào trong CSDL

    Args:
        weather_status_dao (BasicWeatherStatusDAO): Một DAO có thể thao tác với CSDL các trạng thái thời tiết
        new_weather_status (WeatherStatus): Trạng thái thời tiết mới cần được thêm vào
    """
    weather_status_dao.insert(new_weather_status)

def clear(weather_status_dao: BasicWeatherStatusDAO,
          city_id: int) -> None:
    """
    Xóa tất cả các trạng thái thời tiết hiện có của một city trong CSDL

    Args:
        weather_status_dao (BasicWeatherStatusDAO): Một DAO có thể thao tác với CSDL các trạng thái thời tiết
        city_id (int): Mã định danh của thành phố
    """
    weather_status_dao.delete_all(city_id)

def get_status(general_weather_dao: BasicGeneralWeatherDAO,
               status_id: int|list[int]|None) -> list[GeneralWeather]:
    """
    Lấy các kiểu thời tiết được cho phép sử dụng

    Args:
        general_weather_dao (BasicGeneralWeatherDAO): Một DAO có thể thao tác với CSDL các kiểu thời tiết
        status_id (int | list[int] | None): Một hoặc nhiều mã định danh của kiểu thời tiết cần lấy

    Returns:
        list[GeneralWeather]: Danh sách các kiểu thời tiết cần lấy
    """
    # Chuyển đổi tham số đầu vào thành list
    general_weathers: List[GeneralWeather] = []
    if status_id is None:
        general_weathers = general_weather_dao.get_all()
        return general_weathers
    status_id_lst: List[int] = []
    if isinstance(status_id, int):
        status_id_lst.append(status_id)
    else:
        status_id_lst = status_id
    
    # Với mỗi ID trong list thì thực hiện lấy từ CSDL
    for status_id_item in status_id_lst:
        general_weathers.append(general_weather_dao.get(status_id_item))
    
    return general_weathers