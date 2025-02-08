if __name__ == '__main__':
    from etl import auto_weather_vietnam_etl
    auto_weather_vietnam_etl(
        type='minutely',
        job_limits=4,
        dbms='MongoDB',
        minute_frequent=30
    )