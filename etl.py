import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
import sys
sys.path.append(init_dir)
from typing import List

#Place
from place.dao import MySQLCityDAO
from place.business import get_city

#Weather
from weather.model import WeatherStatus
from weather.dao import MySQLWeatherStatusDAO
from weather.business import extract_from_open_weather, transform, load

#Timer & logger
import time
import logging
logging.basicConfig(filename='etl_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def weather_vietnam_etl():
    # Bắt đầu
    logging.info('<<ETL Process>>')
    total_start_time = time.time()
    # Cấu hình các DAO
    logging.info('Config data access object...')
    city_dao = MySQLCityDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
    weather_dao = MySQLWeatherStatusDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
    
    # Lấy dữ liệu tất cả các thành phố
    logging.info('Getting data of all cities of Viet Nam...')
    start_time = time.time()
    try:
        # Trả về list
        cities = get_city(city_dao, type='all_country', country='VN')
    except Exception as e:
        logging.error('Failed to get cities data!!!')
        print(e)
    end_time = time.time()
    msg = f'Successfully. Elapsed Time: {end_time-start_time:.4f}s...'
    logging.info(msg)
    
    # Extract dữ liệu weather
    logging.info(f'Extracting weather data for {len(cities)} cities of Viet Nam...')
    start_time = time.time()
    success = 0
    json_datas: List[dict] = []
    for city in cities:
        try:
            json_datas.append({
                'data': extract_from_open_weather(city.lon, city.lat),
                'city': city
            })
            success += 1
        except Exception as e:
            logging.error(f'Failed to extracting data of {city.name}!!!')
            print(e)
    end_time = time.time()
    msg = f'Successfully extract {success}/{len(cities)}. Elapsed Time: {end_time-start_time:.4f}s...'
    logging.info(msg) 
    for json_data in json_datas:
        print(json_data)
    
    # Transform dữ liệu
    logging.info(f'Transforming weather data for {len(json_datas)} cities of Viet Nam...')
    start_time = time.time()
    success = 0
    new_weather_status_lst: List[WeatherStatus] = []
    for json_data in json_datas:
        try:
            new_weather_status_lst.append(transform(json_data['data'], json_data['city'].city_id))
            success += 1
        except Exception as e:
            logging.error(f"Failed to transforming data of {json_data['city'].name}!!!")
            print(e)
    end_time = time.time()
    msg = f'Successfully transform {success}/{len(json_datas)}. Elapsed Time: {end_time-start_time:.4f}s...'
    logging.info(msg)
    
    # Load into database
    logging.info(f'Loading weather data for {len(new_weather_status_lst)} cities of Viet Nam...')
    start_time = time.time()
    success = 0
    for new_weather_status in new_weather_status_lst:
        try:
            load(weather_dao, new_weather_status)
            success += 1
        except Exception as e:
            logging.error(f'Failed to loading data of city with id {new_weather_status.city_id}!!!')
            print(e)
    end_time = time.time()
    msg = f'Successfully load {success}/{len(new_weather_status_lst)}. Elapsed Time: {end_time-start_time:.4f}s...'
    logging.info(msg)
    
    total_end_time = time.time()
    msg = f'<<End>>. Total Elapsed Time: {total_end_time-total_start_time:.4f}s...'
    logging.info(msg)