if __name__ == '__main__':
    from etl import auto_weather_vietnam_etl
    from datetime import time
    auto_weather_vietnam_etl(
        type='daily',
        job_limits=4,
        dbms='MongoDB',
        daily_collect_time=[time(20, 20, 0), time(21, 10, 0),
                            time(22, 0, 0), time(22, 30, 0)]
    )