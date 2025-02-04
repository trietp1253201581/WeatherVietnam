import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
import sys
sys.path.append(init_dir)
from typing import List, Literal

#Place
from place.dao import MySQLCityDAO
from place.business import get_city

#Weather
from weather.model import WeatherStatus
from weather.dao import MySQLWeatherStatusDAO
from weather.business import extract_from_open_weather, transform, load

import datetime

#Timer & logger
import time
import logging
logging.basicConfig(filename='etl_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

import schedule

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
    
job_cnt = 0
    
def _weather_viet_nam_etl_limited():
    global job_cnt

    job_cnt += 1
    logging.info(f'---Job {job_cnt}---')
    weather_vietnam_etl()

def _supported_3_minutes_job():
    now = datetime.datetime.now()
    if now.minute % 3 == 0:
        _weather_viet_nam_etl_limited()

def _supported_10_minutes_job():
    now = datetime.datetime.now()
    if now.minute % 10 == 0:
        _weather_viet_nam_etl_limited()
        
def _supported_30_minutes_job():
    now = datetime.datetime.now()
    if now.minute % 30 == 0:
        _weather_viet_nam_etl_limited()
        
def auto_weather_vietnam_etl(type: Literal['daily', 'hourly', '30-min', '10-min', '3-min'] = '10-min',
                             job_limits: int|None = None,
                             daily_collect_time: datetime.time|list[datetime.time]|None = None):
    global job_cnt 
    job_cnt = 0
    if type == 'daily':
        if daily_collect_time is None:
            raise ValueError('Daily type required daily collect time!')
        daily_collect_times: List[datetime.time] = []
        if isinstance(daily_collect_time, datetime.time):
            daily_collect_times.append(daily_collect_time)
        else:
            daily_collect_times = daily_collect_time
        for collect_time in daily_collect_times:
            collect_time_str = collect_time.strftime("%H:%M")
            schedule.every().day.at(collect_time_str).do(_weather_viet_nam_etl_limited).tag(type)
    elif type == 'hourly':
        schedule.every().hour.at(":00").do(_weather_viet_nam_etl_limited).tag(type)
    elif type == '30-min':
        schedule.every().minute.at(":00").do(_supported_30_minutes_job).tag(type)
    elif type == '10-min':
        schedule.every().minute.at(":00").do(_supported_10_minutes_job).tag(type)
    elif type == '3-min':
        schedule.every().minute.at(":00").do(_supported_3_minutes_job).tag(type)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
        if job_limits is not None and job_cnt >= job_limits:
            logging.info(f"Execution job count has reached {job_limits}. Cancelling the job.")
            schedule.clear(type)
            break
    
    logging.info('!!!Done!!!')
        