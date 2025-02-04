if __name__ == '__main__':
    from etl import auto_weather_vietnam_etl
    auto_weather_vietnam_etl(
        type='3-min',
        job_limits=3
    )
