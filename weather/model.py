"""
Module `model` cung cấp class để đại diện
cho các dữ liệu thời tiết, bao gồm các kiểu thời tiết
và trạng thái thời tiết của các thành phố.

Author: 
    Lê Minh Triết
Last Modified Date: 
    04/02/2025
"""

from datetime import datetime

class GeneralWeather:
    """
    Đại diện cho một kiểu thời tiết chung.
    """
    
    def __init__(self, status_id: int, description: str|None = None):
        """
        Khởi tạo 1 đối tượng thời tiết chung.

        Args:
            status_id (int): Mã định danh của kiểu thời tiết
            description (str | None, optional): Diễn giải về kiểu thời tiết. Defaults to None.
        """
        self.status_id = status_id
        self.description = description
    
    @property
    def status_id(self):
        return self.__status_id
    
    @property
    def description(self):
        return self.__description
    
    @status_id.setter
    def status_id(self, status_id: int):
        self.__status_id = status_id
    
    @description.setter
    def description(self, description: str|None):
        self.__description = description
    
    def __str__(self):
        s = f'GeneralWeather('
        s += f'status_id={self.__status_id}, '
        s += f'description={self.__description}'
        s += f')'
        return s
    
    @staticmethod
    def from_tuple(source: tuple[int, str|None]) -> 'GeneralWeather':
        """
        Lấy một General Weather từ một tuple

        Args:
            source (tuple[int, str | None]): một tuple có dạng (status_id, description)

        Raises:
            ValueError: Nếu tuple ban đầu không có đủ 2 thành phần

        Returns:
            GeneralWeather: Đối tượng thu được
        """
        if len(source) == 0:
            return None
        if len(source) != 2:
            raise ValueError("Invalid argurment, required 2 argument!")
        return GeneralWeather(
            status_id=source[0],
            description=source[1]
        )
    
    def to_tuple(self) -> tuple[int, str|None]:
        """
        Chuyển đối tượng hiện tại sang một tuple

        Returns:
            tuple[int, str|None]: Một tuple có dạng (status_id, description)
        """
        return self.__status_id, self.__description

class WeatherStatus:
    """
    Đối tượng đại diện cho trạng thái thời tiết được thu thập từ các thành phố.
    """
    
    def __init__(self, city_id: int, collect_time: datetime,
                 temp: float|None = None, feels_temp: float|None = None,
                 pressure: int|None = None, humidity: int|None = None,
                 sea_level: int|None = None, grnd_level: int|None = None,
                 visibility: int|None = None, wind_speed: float|None = None,
                 wind_deg: int|None = None, wind_gust: float|None = None,
                 clouds_all: int|None = None, rain: float|None = None,
                 sunrise: datetime|None = None, sunset: datetime|None = None,
                 aqi: int|None = None, pm2_5: float|None = None,
                 general_weathers: list[GeneralWeather] = [],
                 max_decimal: int = 7):
        """
        Khởi tạo một trạng thái thời tiết của một thành phố.

        Args:
            city_id (int): Id của thành phố được thu thập trạng thái.
            collect_time (datetime): Thời điểm thu thập trạng thái thời tiết.
            temp (float | None, optional): Nhiệt độ (Kelvin), không âm.
            feels_temp (float | None, optional): Nhiệt độ cảm nhận được (Kelvin), không âm. Defaults to None.
            pressure (int | None, optional): Áp suất khí quyển (hPa), không âm. Defaults to None.
            humidity (int | None, optional): Độ ẩm không khí (%), từ 0-100. Defaults to None.
            sea_level (int | None, optional): Áp suất tại mực nước biển (hPa), không âm. Defaults to None.
            grnd_level (int | None, optional): Áp suất tại mặt đất (hPa), không âm. Defaults to None.
            visibility (int | None, optional): Tầm nhìn xa (mét), không âm. Defaults to None.
            wind_speed (float | None, optional): Tốc độ gió (m/s), không âm. Defaults to None.
            wind_deg (int | None, optional): Hướng gió (độ), từ 0-360. Defaults to None.
            wind_gust (float | None, optional): Giật gió (m/s), không âm. Defaults to None.
            clouds_all (int | None, optional): Độ bao phủ mây (%), từ 0-100. Defaults to None.
            rain (float | None, optional): Lượng mưa (mm/h), không âm. Defaults to None.
            sunrise (datetime | None, optional): Thời gian mặt trời mọc. Defaults to None.
            sunset (datetime | None, optional): Thời gian mặt trời lặn. Defaults to None.
            aqi (int | None, optional): Chỉ số AQI (1, 2, 3, 4 hoặc 5). Defaults to None.
            pm2_5 (float | None, optional): Nồng độ bụi PM 2.5 (μg/m^3), không âm. Defaults to None.
            general_weathers (list[GeneralWeather], optional): Danh sách các kiểu thời tiết chung hiện tại. Defaults to [].
            max_decimal (int, optional): Số lượng số sau dấu phẩy lấy chính xác của các thuộc tính float. Defaults to 7.
        """
        self.max_decimal = max_decimal
        self.city_id = city_id
        self.collect_time = collect_time
        self.temp = temp
        self.feels_temp = feels_temp
        self.pressure = pressure
        self.humidity = humidity
        self.sea_level = sea_level
        self.grnd_level = grnd_level
        self.visibility = visibility
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg
        self.wind_gust = wind_gust
        self.clouds_all = clouds_all
        self.rain = rain
        self.sunrise = sunrise
        self.sunset = sunset
        self.aqi = aqi
        self.pm2_5 = pm2_5
        self.general_weathers = general_weathers

    @property
    def city_id(self):
        return self.__city_id
    
    @property
    def collect_time(self):
        return self.__collect_time

    @property
    def temp(self):
        return self.__temp
    
    @property
    def feels_temp(self):
        return self.__feels_temp

    @property
    def pressure(self):
        return self.__pressure
    
    @property
    def humidity(self):
        return self.__humidity
    
    @property
    def sea_level(self):
        return self.__sea_level

    @property
    def grnd_level(self):
        return self.__grnd_level
    
    @property
    def visibility(self):
        return self.__visibility
    
    @property
    def wind_speed(self):
        return self.__wind_speed
    
    @property
    def wind_deg(self):
        return self.__wind_deg
    
    @property
    def wind_gust(self):
        return self.__wind_gust
    
    @property
    def clouds_all(self):
        return self.__clouds_all
    
    @property
    def rain(self):
        return self.__rain
    
    @property
    def sunrise(self):
        return self.__sunrise
    
    @property
    def sunset(self):
        return self.__sunset
    
    @property
    def aqi(self):
        return self.__aqi
    
    @property
    def pm2_5(self):
        return self.__pm2_5
    
    @property
    def general_weathers(self):
        return self.__general_weathers
    
    @property
    def max_decimal(self):
        return self.__max_decimal

    @city_id.setter
    def city_id(self, city_id: int):
        self.__city_id = city_id
    
    @collect_time.setter
    def collect_time(self, collect_time: datetime):
        self.__collect_time = collect_time

    @temp.setter
    def temp(self, temp: float|None):
        if temp is None: 
            self.__temp = None
        else:
            if temp < 0:
                raise ValueError("Temp is non-negative!")
            else:
                self.__temp = float(round(temp, self.__max_decimal))
    
    @feels_temp.setter
    def feels_temp(self, feels_temp: float|None):
        if feels_temp is None:
            self.__feels_temp = None
        else:
            if feels_temp < 0:
                raise ValueError("Temp is non-negative!")
            else:
                self.__feels_temp = float(round(feels_temp, self.__max_decimal))

    @pressure.setter
    def pressure(self, pressure: int|None):
        if isinstance(pressure, int) and pressure < 0:
            raise ValueError("Pressure is non-negative!")
        self.__pressure = pressure
    
    @humidity.setter
    def humidity(self, humidity: int|None):
        self.__humidity = humidity
    
    @sea_level.setter
    def sea_level(self, sea_level: int|None):
        if isinstance(sea_level, int) and sea_level < 0:
            raise ValueError("Pressure at sea level is non-negative!")
        self.__sea_level = sea_level

    @grnd_level.setter
    def grnd_level(self, grnd_level: int|None):
        if isinstance(grnd_level, int) and grnd_level < 0:
            raise ValueError("Pressure at grnd level is non-negative!")
        self.__grnd_level = grnd_level
    
    @visibility.setter
    def visibility(self, visibility: int|None):
        if isinstance(visibility, int) and visibility < 0:
            raise ValueError("Visibility is non-negative!")
        self.__visibility = visibility
    
    @wind_speed.setter
    def wind_speed(self, wind_speed: float|None):
        if wind_speed is None:
            self.__wind_speed = None
        else:
            if wind_speed < 0:
                raise ValueError("Wind speed is non-negative!")
            else:
                self.__wind_speed = float(round(wind_speed, self.__max_decimal))
    
    @wind_deg.setter
    def wind_deg(self, wind_deg: int|None):
        if isinstance(wind_deg, int) and (wind_deg < 0 or wind_deg > 360):
            raise ValueError("Wind degree is in [0, 360]!") 
        self.__wind_deg = wind_deg
    
    @wind_gust.setter
    def wind_gust(self, wind_gust: float|None):
        if wind_gust is None:
            self.__wind_gust = None
        else:
            if wind_gust < 0:
                raise ValueError("Wind gust is non-negative!")
            else:
                self.__wind_gust = float(round(wind_gust, self.__max_decimal))
    
    @clouds_all.setter
    def clouds_all(self, clouds_all: int|None):
        if isinstance(clouds_all, int) and (clouds_all < 0 or clouds_all > 100):
            raise ValueError("Clouds percent is in [0, 100]!") 
        self.__clouds_all = clouds_all
    
    @rain.setter
    def rain(self, rain: float|None):
        if rain is None:
            self.__rain = None
        else: 
            if rain < 0:
                raise ValueError("Rain is non-negative!")
            else:
                self.__rain = float(round(rain, self.__max_decimal))
    
    @sunrise.setter
    def sunrise(self, sunrise: datetime|None):
        self.__sunrise = sunrise
    
    @sunset.setter
    def sunset(self, sunset: datetime|None):
        self.__sunset = sunset
    
    @aqi.setter
    def aqi(self, aqi: int|None):
        if isinstance(aqi, int) and (aqi < 1 or aqi > 5):
             raise ValueError("AQI is in (1,2,3,4,5)")
        self.__aqi = aqi
    
    @pm2_5.setter
    def pm2_5(self, pm2_5: float|None):
        if pm2_5 is None:
            self.__pm2_5 = None
        else:
            if pm2_5 < 0:
                raise ValueError("PM2.5 is non-negative!")
            else:
                self.__pm2_5 = float(round(pm2_5, self.__max_decimal))
        
    @general_weathers.setter
    def general_weathers(self, general_weathers: list[GeneralWeather] = []):
        self.__general_weathers = general_weathers
        
    @max_decimal.setter
    def max_decimal(self, max_decimal: int):
        if max_decimal < 0:
            raise ValueError("Max decimal is non-negative!")
        self.__max_decimal = max_decimal

    def __str__(self):
        s = f'WeatherStatus('
        s += f'city_id={self.__city_id},' 
        s += f'collect_time={self.__collect_time}, '
        s += f'temp={self.__temp}, '
        s += f'feels_temp={self.__feels_temp}, '
        s += f'pressure={self.__pressure}, '
        s += f'humidity={self.__humidity}, '
        s += f'sea_level={self.__sea_level}, '
        s += f'grnd_level={self.__grnd_level}, '
        s += f'visibility={self.__visibility}, '
        s += f'wind_speed={self.__wind_speed}, '
        s += f'wind_deg={self.__wind_deg}, '
        s += f'wind_gust={self.__wind_gust}, '
        s += f'clouds_all={self.__clouds_all}, '
        s += f'rain={self.__rain}, '
        s += f'sunrise={self.__sunrise}, '
        s += f'sunset={self.__sunset}, '
        s += f'aqi={self.__aqi}, ' 
        s += f'pm2_5={self.__pm2_5}, '
        s += f'general_weathers=[{", ".join(str(general_weather) for general_weather in self.__general_weathers)}]'
        s += ')'
        return s

    @staticmethod
    def from_tuple(source: tuple) -> 'WeatherStatus':
        """
        Chuyển một tuple sang một đối tượng Weather Status

        Args:
            source (tuple): Một tuple có dạng sau:
                (city_id, collect_time, temp, feels_temp, pressure, humidity, sea_level, grnd_level, visibility, 
                wind_speed, wind_deg, wind_gust, clouds_all, rain, sunrise, sunset, aqi, pm2_5, 
                general_weathers (a list of tuple))

        Raises:
            ValueError: Khi tuple không có đủ 19 thành phần

        Returns:
            WeatherStatus: Trạng thái thời tiết thu được
        """
        if len(source) == 0:
            return None
        if len(source) != 19:
            raise ValueError("Invalid argument, required 19 arguments!")
        return WeatherStatus(
            city_id=source[0],
            collect_time=source[1],
            temp=source[2],
            feels_temp=source[3],
            pressure=source[4],
            humidity=source[5],
            sea_level=source[6],
            grnd_level=source[7],
            visibility=source[8],
            wind_speed=source[9],
            wind_deg=source[10],
            wind_gust=source[11],
            clouds_all=source[12],
            rain=source[13],
            sunrise=source[14],
            sunset=source[15],
            aqi=source[16],
            pm2_5=source[17],
            general_weathers=[GeneralWeather.from_tuple(item) for item in source[18]],
        )

    def to_tuple(self) -> tuple:
        """
        Chuyển đối tượng hiện tại thành 1 tuple
        
        Returns:
            tuple: Một tuple có dạng sau:
                (city_id, collect_time, temp, feels_temp, pressure, humidity, sea_level, grnd_level, visibility, 
                wind_speed, wind_deg, wind_gust, clouds_all, rain, sunrise, sunset, aqi, pm2_5, 
                general_weathers (a list of tuple))
        """
        return (self.__city_id, self.__collect_time, self.__temp, self.__feels_temp, self.__pressure, 
                self.__humidity, self.__sea_level, self.__grnd_level, self.__visibility, self.__wind_speed, 
                self.__wind_deg, self.__wind_gust, self.__clouds_all, self.__rain, self.__sunrise, 
                self.__sunset, self.__aqi, self.__pm2_5, 
                [general_weather.to_tuple() for general_weather in self.__general_weathers])