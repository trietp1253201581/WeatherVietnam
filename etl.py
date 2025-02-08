"""
Module `etl` cung cấp các quy trình ETL thủ công hoặc tự động
để thực hiện lấy, chuyển đồi và lưu vào CSDL dữ liệu các
trạng thái thời tiết của các thành phố ở Việt Nam.

Author: 
    Lê Minh Triết
Last Modified Date: 
    04/02/2025
"""

import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
import sys
sys.path.append(init_dir)

from typing import List, Literal

#Place
from place.dao import MySQLCityDAO, MongoDBCityDAO
from place.business import get_city

#Weather
from weather.model import WeatherStatus
from weather.dao import MySQLWeatherStatusDAO, MongoDBWeatherStatusDAO
from weather.business import extract_from_open_weather, transform, load

import datetime

#Timer & logger
import time
import logging
logging.basicConfig(filename='etl_log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

import schedule
from functools import partial

def weather_vietnam_etl(dbms: Literal['MySQL', 'MongoDB'] = 'MySQL'):
    """
    Quy trình ETL thủ công để làm việc với dữ liệu thời tiết các thành phố Việt Nam

    Args:
        dbms (Literal[&#39;MySQL&#39;, &#39;MongoDB&#39;], optional): Hệ quản trị CSDL
            được sử dụng để lưu trữ CSDL. Defaults to 'MySQL'.
    """
    # Bắt đầu
    logging.info('<<ETL Process>>')
    total_start_time = time.time()
    
    # Cấu hình các DAO
    logging.info('Config data access object...')
    if dbms == 'MySQL':
        city_dao = MySQLCityDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
        weather_dao = MySQLWeatherStatusDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
    else:
        city_dao = MongoDBCityDAO('localhost', 27017, 'weather_vietnam')
        weather_dao = MongoDBWeatherStatusDAO('localhost', 27017, 'weather_vietnam')
    
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
    # Với mỗi thành phố, thực hiện extract và thêm vào list các JSON
    # Nếu có một thành phố bị lỗi thì vẫn extract tiếp và chỉ thông báo ERROR ra log
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
    # Chỉ transform dữ liệu những thành phố được extract thành công
    # Nếu có thành phố nào bị chuyển đối lỗi thì vẫn tiếp tục và chỉ ghi log ERROR
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
    # Chỉ thực hiện load những dữ liệu đã được transform thành công
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
    
    # Tổng kết job
    total_end_time = time.time()
    msg = f'<<End>>. Total Elapsed Time: {total_end_time-total_start_time:.4f}s...'
    logging.info(msg)

_job_cnt = 0
    
def _weather_viet_nam_etl_limited(dbms: Literal['MySQL', 'MongoDB'] = 'MySQL'):
    """
    Quy trình được thực hiện cùng với việc tăng bộ đếm Job
    
    Args:
        dbms (Literal[&#39;MySQL&#39;, &#39;MongoDB&#39;], optional): Hệ quản trị CSDL
            được sử dụng để lưu trữ CSDL. Defaults to 'MySQL'.
    """
    global _job_cnt

    _job_cnt += 1
    logging.info(f'---Job {_job_cnt}---')
    weather_vietnam_etl(dbms)
    
def _supported_minutes_job(frequent: int = 1,
                           dbms: Literal['MySQL', 'MongoDB'] = 'MySQL'):
    """
    Quy trình ETL hỗ trợ check tròn phút cộng với tăng bộ đếm

    Args:
        frequent (int, optional): Số phút tròn để thực hiện (1-59).
            Job sẽ được thực hiện vào thời điểm mà phút chia hết
            cho frequent. Defaults to 1.
        dbms (Literal[&#39;MySQL&#39;, &#39;MongoDB&#39;], optional): _description_. Defaults to 'MySQL'.
    """
    now = datetime.datetime.now()
    if now.minute % frequent == 0:
        _weather_viet_nam_etl_limited(dbms)
        
def auto_weather_vietnam_etl(type: Literal['daily', 'hourly', 'minutely'] = 'hourly',
                             job_limits: int|None = None,
                             daily_collect_time: datetime.time|list[datetime.time]|None = None,
                             minute_frequent: int|None = None,
                             dbms: Literal['MySQL', 'MongoDB'] = 'MySQL'):
    """
    Quy trình ETL tự động để thao tác với dữ liệu thời tiết các thành phố ở Việt Nam

    Args:
        type (Literal[&#39;daily&#39;, &#39;hourly&#39;, &#39;minutely&#39;, optional): Tần suất lấy dữ liệu. Defaults to '10-min'.
            `'daily'` 
                Hàng ngày, có thể vào các khung giờ nhất định, lúc này tham số `daily_collect_time` phải được sử dụng.
            `'hourly'`
                Hàng giờ, sẽ lấy chẵn giờ, tức là vào 0h, 1h, 2h,....
            `'minutely'`
                Tròn phút, sẽ lấy vào các phút chia hết cho minute_frequent. Lúc này yêu cầu
                tham số `minute_frequent`.
        job_limits (int | None, optional): Giới hạn số công việc thực hiện. Defaults to None.
        daily_collect_time (datetime.time | list[datetime.time] | None, optional): Thời
            điểm lấy dữ liệu hàng ngày. Defaults to None.
        minute_frequent (int | None, optional): Số phút tròn để lấy dữ liệu. Defaults to None.
        dbms (Literal[&#39;MySQL&#39;, &#39;MongoDB&#39;], optional): Hệ quản trị CSDL
            được sử dụng để lưu trữ CSDL. Defaults to 'MySQL'.

    Raises:
        ValueError: Khi chọn `type='daily'` mà không có tham số `daily_collect_time`, hoặc khi chọn
            `type='minutely'` mà không có tham số `minute_frequent`.
    """
    global _job_cnt 
    _job_cnt = 0
    
    # Tùy thuộc vào type mà lên lịch kế hoạch hoạt động bằng schedule
    # Sẽ gọi các hàm wrapper tương ứng của quy trình ETL thủ công
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
            job = partial(_weather_viet_nam_etl_limited, dbms)
            schedule.every().day.at(collect_time_str).do(job).tag(type)
    elif type == 'hourly':
        job = partial(_weather_viet_nam_etl_limited, dbms)
        schedule.every().hour.at(":00").do(job).tag(type)
    elif type == 'minutely':
        if minute_frequent is None:
            raise ValueError("Required minute frequent!")
        job = partial(_supported_minutes_job, minute_frequent, dbms)
        schedule.every().minute.at(":00").do(job).tag(type)
    else:
        raise ValueError("Not supported type")
    
    # Thực hiện các job theo kế hoạch định trước, chỉ dừng khi đạt giới hạn số lượng.
    while True:
        schedule.run_pending()
        time.sleep(1)
        if job_limits is not None and _job_cnt >= job_limits:
            logging.info(f"Execution job count has reached {job_limits}. Cancelling the job.")
            schedule.clear(type)
            break
    
    logging.info('!!!Done!!!')