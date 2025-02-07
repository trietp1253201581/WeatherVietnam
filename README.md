# WeatherVietnam
## Các thư viện được sử dụng
Có thể cần cài đặt các thư viện logging, typing, json, requests, schedule, mysql-connector
```bash
pip install logging, typing, json, requests, schedule, mysql-connector
```
## Cấu trúc dự án
Bao gồm các module và file sau, chi tiết nhiệm vụ tương ứng đã có trong từng module:
* [main.py](main.py) (file chính để chạy)
* [etl.py](etl.py) (chứa các hàm chính để thực hiện nghiệp vụ ETL)
* [etl_log.log](etl_log.log) (ghi lại log các quy trình ETL)
* `common`: 
  * [dao.py](common/dao.py) (chứa các basic dao để kết nối với các DBMS như MySQL và MongoDB)
* `place`: Các nghiệp vụ liên quan tới địa lý.
  * [model.py](place/model.py)
  * [dao.py](place/dao.py)
  * [business.py](place/business.py)
* `weather`: Các nghiệp vụ liên quan tới dữ liệu thời tiết.
  * [model.py](weather/model.py)
  * [dao.py](weather/dao.py)
  * [business.py](weather/business.py)

Với `place` và `weather` thì `model`, `dao`, `business` lần lượt đại diện cho các mô hình logic, các DAO và các hàm phục vụ nghiệp vụ của các module này.
## Dữ liệu
Dữ liệu về thời tiết của các thành phố ở Việt Nam được lấy từ API của OpenWeatherMap.

Dữ liệu gốc là một JSON Object, được lấy từ API của OpenWeatherMap có dạng sau:

`https://api.openweathermap.org/data/2.5/weather?lat=...&lon=...&apiid=api_key`

trong đó lat, lon là tọa độ của thành phố cần lấy.
aa
Để lấy lat và lon của một thành phố, dùng api

`http://api.openweathermap.org/geo/1.0/direct?q=..country_code..,..city_name..,&limit=1&appid=api_key`

trong đó country_code là Code của quốc gia theo ISO 3166-1 alpha-2, city name là tên viết cách không dấu của tỉnh/thành phố.

Chi tiết về dữ liệu xem ở file [db_info.md](db/db_info.md)

API Key của tôi được lưu giữ trong `config.json`, được ẩn đi để tăng tính bảo mật (thêm vào .gitignore).
## Môi trường phát triển
* Python 3.11.9
* Visual Studio Code
* MySQL 8.0
## Chạy
Chạy file [main.py](main.py)
```bash
python -u main.py
```
hoặc
```bash
& your/path/to/python3.11.exe main.py
```
## Đánh giá độ phức tạp qua radon
Cài đặt radon
```bash
pip install radon
```
### Độ phức tạp CC
Thực hiện lệnh để đo CC
```bash
radon cc . -a -s
```
Kết quả thu được
```bash
etl.py
    F 165:0 auto_weather_vietnam_etl - B (10)
    F 40:0 weather_vietnam_etl - B (9)
    F 150:0 _supported_minutes_job - A (2)
    F 136:0 _weather_viet_nam_etl_limited - A (1)
common\dao.py
    M 163:4 BasicMongoDBDAO.connect_ - B (6)
    M 103:4 BasicMySQLDAO.get_sql_file_reader_ - A (5)
    C 141:0 BasicMongoDBDAO - A (5)
    C 55:0 BasicMySQLDAO - A (3)
    C 27:0 DAOException - A (2)
    C 41:0 NotExistDataException - A (2)
    M 79:4 BasicMySQLDAO.connect_ - A (2)
    M 32:4 DAOException.__init__ - A (1)
    M 46:4 NotExistDataException.__init__ - A (1)
    M 62:4 BasicMySQLDAO.__init__ - A (1)
    M 135:4 BasicMySQLDAO.close_connection - A (1)
    M 147:4 BasicMongoDBDAO.__init__ - A (1)
db\info.py
    C 21:0 CityEnableQueries - A (1)
    C 30:0 CountryEnableQueries - A (1)
    C 35:0 GeneralWeatherEnableQueries - A (1)
    C 39:0 WeatherStatusEnableQueries - A (1)
    C 46:0 WeatherConditionEnableQueries - A (1)
db\sql_reader.py
    M 39:4 SQLFileReader.read - B (9)
    C 28:0 SQLFileReader - A (4)
    C 13:0 NotSupportedQueryException - A (2)
    M 93:4 SQLFileReader.get_query_of - A (2)
    F 48:0 _get_city - A (4)
    F 71:0 _get_all_of_country - A (4)
    F 126:0 insert_city - A (3)
    F 24:0 extract_from_open_weather - A (1)
    F 168:0 get_country - A (1)
place\dao.py
    M 242:4 MySQLCityDAO.get - B (8)
    C 218:0 MySQLCityDAO - A (5)
    M 288:4 MySQLCityDAO.insert - A (5)
    M 450:4 MongoDBCityDAO.get - A (5)
    M 477:4 MongoDBCityDAO.insert - A (5)
    C 65:0 MySQLCountryDAO - A (4)
    M 86:4 MySQLCountryDAO.get - A (4)
    M 114:4 MySQLCountryDAO.insert - A (4)
    M 136:4 MySQLCountryDAO.delete - A (4)
    M 316:4 MySQLCityDAO.delete - A (4)
    M 338:4 MySQLCityDAO.get_all - A (4)
    C 426:0 MongoDBCityDAO - A (4)
    C 372:0 MongoDBCountryDAO - A (3)
    M 405:4 MongoDBCountryDAO.insert - A (3)
    C 26:0 BasicCountryDAO - A (2)
    C 162:0 BasicCityDAO - A (2)
    M 395:4 MongoDBCountryDAO.get - A (2)
    M 417:4 MongoDBCountryDAO.delete - A (2)
    M 504:4 MongoDBCityDAO.delete - A (2)
    M 513:4 MongoDBCityDAO.get_all - A (2)
    M 33:4 BasicCountryDAO.get - A (1)
    M 47:4 BasicCountryDAO.insert - A (1)
    M 57:4 BasicCountryDAO.delete - A (1)
    M 71:4 MySQLCountryDAO.__init__ - A (1)
    M 169:4 BasicCityDAO.get - A (1)
    M 186:4 BasicCityDAO.insert - A (1)
    M 196:4 BasicCityDAO.delete - A (1)
    M 205:4 BasicCityDAO.get_all - A (1)
    M 224:4 MySQLCityDAO.__init__ - A (1)
    M 378:4 MongoDBCountryDAO.__init__ - A (1)
    M 432:4 MongoDBCityDAO.__init__ - A (1)
place\model.py
    M 46:4 Country.code - A (4)
    M 65:4 Country.get_code_with_type - A (4)
    M 273:4 City.__str__ - A (4)
    M 130:4 Country.from_tuple - A (3)
    M 261:4 City.time_zone - A (3)
    M 285:4 City.from_tuple - A (3)
    C 15:0 Country - A (2)
    M 20:4 Country.__init__ - A (2)
    M 90:4 Country.get_iso_name - A (2)
    M 106:4 Country.get_offical_name - A (2)
    C 191:0 City - A (2)
    M 38:4 Country.code - A (1)
    M 42:4 Country.name - A (1)
    M 62:4 Country.name - A (1)
    M 122:4 Country.__str__ - A (1)
    M 153:4 Country.to_tuple - A (1)
    M 163:4 Country.from_json - A (1)
    M 257:4 City.lon - A (1)
    M 267:4 City.country - A (1)
    M 270:4 City.get_coord - A (1)
    M 312:4 City.to_tuple - A (1)
    M 323:4 City.from_json - A (1)
    M 344:4 City.to_json - A (1)
weather\business.py
    F 67:0 transform - A (4)
    F 132:0 get_status - A (4)
    F 25:0 extract_from_open_weather - A (1)
    F 110:0 load - A (1)
    F 121:0 clear - A (1)
weather\dao.py
    C 187:0 MySQLWeatherStatusDAO - A (5)
    M 212:4 MySQLWeatherStatusDAO.get - A (5)
    M 255:4 MySQLWeatherStatusDAO.get_all - A (5)
    M 301:4 MySQLWeatherStatusDAO.insert - A (5)
    C 55:0 MySQLGeneralWeatherDAO - A (4)
    M 76:4 MySQLGeneralWeatherDAO.get - A (4)
    M 99:4 MySQLGeneralWeatherDAO.get_all - A (4)
    M 340:4 MySQLWeatherStatusDAO.delete - A (4)
    M 362:4 MySQLWeatherStatusDAO.delete_all - A (4)
    M 505:4 MongoDBWeatherStatusDAO.insert - A (4)
    C 384:0 MongoDBGeneralWeatherDAO - A (3)
    C 426:0 MongoDBWeatherStatusDAO - A (3)
    M 450:4 MongoDBWeatherStatusDAO.get - A (3)
    M 478:4 MongoDBWeatherStatusDAO.get_all - A (3)
    M 417:4 MongoDBGeneralWeatherDAO.get_all - A (2)
    M 525:4 MongoDBWeatherStatusDAO.delete - A (2)
    M 537:4 MongoDBWeatherStatusDAO.delete_all - A (2)
    M 33:4 BasicGeneralWeatherDAO.get - A (1)
    M 46:4 BasicGeneralWeatherDAO.get_all - A (1)
    M 61:4 MySQLGeneralWeatherDAO.__init__ - A (1)
    M 130:4 BasicWeatherStatusDAO.get - A (1)
    M 144:4 BasicWeatherStatusDAO.get_all - A (1)
    M 157:4 BasicWeatherStatusDAO.insert - A (1)
    M 167:4 BasicWeatherStatusDAO.delete - A (1)
    M 178:4 BasicWeatherStatusDAO.delete_all - A (1)
    M 193:4 MySQLWeatherStatusDAO.__init__ - A (1)
    M 390:4 MongoDBGeneralWeatherDAO.__init__ - A (1)
    M 432:4 MongoDBWeatherStatusDAO.__init__ - A (1)
weather\model.py
    M 324:4 WeatherStatus.wind_deg - A (4)
    M 340:4 WeatherStatus.clouds_all - A (4)
    M 372:4 WeatherStatus.aqi - A (4)
    M 422:4 WeatherStatus.from_tuple - A (4)
    M 54:4 GeneralWeather.from_tuple - A (3)
    M 266:4 WeatherStatus.temp - A (3)
    M 276:4 WeatherStatus.feels_temp - A (3)
    M 286:4 WeatherStatus.pressure - A (3)
    M 296:4 WeatherStatus.sea_level - A (3)
    M 302:4 WeatherStatus.grnd_level - A (3)
    M 308:4 WeatherStatus.visibility - A (3)
    M 314:4 WeatherStatus.wind_speed - A (3)
    M 330:4 WeatherStatus.wind_gust - A (3)
    M 346:4 WeatherStatus.rain - A (3)
    M 378:4 WeatherStatus.pm2_5 - A (3)
    C 14:0 GeneralWeather - A (2)
    C 114:0 WeatherStatus - A (2)
    M 356:4 WeatherStatus.sunrise - A (2)
    M 364:4 WeatherStatus.sunset - A (2)
    M 392:4 WeatherStatus.max_decimal - A (2)
    M 397:4 WeatherStatus.__str__ - A (2)
    M 464:4 WeatherStatus.to_tuple - A (2)
    M 481:4 WeatherStatus.from_json - A (2)
    M 516:4 WeatherStatus.to_json - A (2)
    M 19:4 GeneralWeather.__init__ - A (1)
    M 31:4 GeneralWeather.status_id - A (1)
    M 35:4 GeneralWeather.description - A (1)
    M 39:4 GeneralWeather.status_id - A (1)
    M 43:4 GeneralWeather.description - A (1)
    M 46:4 GeneralWeather.__str__ - A (1)
    M 76:4 GeneralWeather.to_tuple - A (1)
    M 86:4 GeneralWeather.from_json - A (1)
    M 102:4 GeneralWeather.to_json - A (1)
    M 119:4 WeatherStatus.__init__ - A (1)
    M 177:4 WeatherStatus.city_id - A (1)
    M 181:4 WeatherStatus.collect_time - A (1)
    M 185:4 WeatherStatus.temp - A (1)
    M 189:4 WeatherStatus.feels_temp - A (1)
    M 193:4 WeatherStatus.pressure - A (1)
    M 197:4 WeatherStatus.humidity - A (1)
    M 201:4 WeatherStatus.sea_level - A (1)
    M 205:4 WeatherStatus.grnd_level - A (1)
    M 209:4 WeatherStatus.visibility - A (1)
    M 213:4 WeatherStatus.wind_speed - A (1)
    M 217:4 WeatherStatus.wind_deg - A (1)
    M 221:4 WeatherStatus.wind_gust - A (1)
    M 225:4 WeatherStatus.clouds_all - A (1)
    M 229:4 WeatherStatus.rain - A (1)
    M 233:4 WeatherStatus.sunrise - A (1)
    M 237:4 WeatherStatus.sunset - A (1)
    M 241:4 WeatherStatus.aqi - A (1)
    M 221:4 WeatherStatus.wind_gust - A (1)
    M 225:4 WeatherStatus.clouds_all - A (1)
    M 229:4 WeatherStatus.rain - A (1)
    M 233:4 WeatherStatus.sunrise - A (1)
    M 237:4 WeatherStatus.sunset - A (1)
    M 241:4 WeatherStatus.aqi - A (1)
    M 245:4 WeatherStatus.pm2_5 - A (1)
    M 249:4 WeatherStatus.general_weathers - A (1)
    M 253:4 WeatherStatus.max_decimal - A (1)
    M 257:4 WeatherStatus.city_id - A (1)
    M 261:4 WeatherStatus.collect_time - A (1)
    M 221:4 WeatherStatus.wind_gust - A (1)
    M 225:4 WeatherStatus.clouds_all - A (1)
    M 229:4 WeatherStatus.rain - A (1)
    M 233:4 WeatherStatus.sunrise - A (1)
    M 237:4 WeatherStatus.sunset - A (1)
    M 241:4 WeatherStatus.aqi - A (1)
    M 245:4 WeatherStatus.pm2_5 - A (1)
    M 249:4 WeatherStatus.general_weathers - A (1)
    M 253:4 WeatherStatus.max_decimal - A (1)
    M 257:4 WeatherStatus.city_id - A (1)
    M 221:4 WeatherStatus.wind_gust - A (1)
    M 225:4 WeatherStatus.clouds_all - A (1)
    M 229:4 WeatherStatus.rain - A (1)
    M 233:4 WeatherStatus.sunrise - A (1)
    M 237:4 WeatherStatus.sunset - A (1)
    M 241:4 WeatherStatus.aqi - A (1)
    M 245:4 WeatherStatus.pm2_5 - A (1)
    M 225:4 WeatherStatus.clouds_all - A (1)
    M 229:4 WeatherStatus.rain - A (1)
    M 233:4 WeatherStatus.sunrise - A (1)
    M 237:4 WeatherStatus.sunset - A (1)
    M 241:4 WeatherStatus.aqi - A (1)
    M 245:4 WeatherStatus.pm2_5 - A (1)
    M 249:4 WeatherStatus.general_weathers - A (1)
    M 237:4 WeatherStatus.sunset - A (1)
    M 241:4 WeatherStatus.aqi - A (1)
    M 245:4 WeatherStatus.pm2_5 - A (1)
    M 249:4 WeatherStatus.general_weathers - A (1)
    M 253:4 WeatherStatus.max_decimal - A (1)
    M 257:4 WeatherStatus.city_id - A (1)
    M 241:4 WeatherStatus.aqi - A (1)
    M 245:4 WeatherStatus.pm2_5 - A (1)
    M 249:4 WeatherStatus.general_weathers - A (1)
    M 253:4 WeatherStatus.max_decimal - A (1)
    M 257:4 WeatherStatus.city_id - A (1)
    M 261:4 WeatherStatus.collect_time - A (1)
    M 245:4 WeatherStatus.pm2_5 - A (1)
    M 249:4 WeatherStatus.general_weathers - A (1)
    M 253:4 WeatherStatus.max_decimal - A (1)
    M 257:4 WeatherStatus.city_id - A (1)
    M 261:4 WeatherStatus.collect_time - A (1)
    M 253:4 WeatherStatus.max_decimal - A (1)
    M 257:4 WeatherStatus.city_id - A (1)
    M 261:4 WeatherStatus.collect_time - A (1)
    M 261:4 WeatherStatus.collect_time - A (1)
    M 292:4 WeatherStatus.humidity - A (1)
    M 292:4 WeatherStatus.humidity - A (1)
    M 388:4 WeatherStatus.general_weathers - A (1)

195 blocks (classes, functions, methods) analyzed.
Average complexity: A (2.230769230769231)
```

### Số lượng dòng code
Về số dòng code, chạy lệnh
```bash
radon raw . -s
```
Kết quả thu được
```bash
etl.py
    LOC: 227
    LLOC: 130
    SLOC: 131
    Comments: 19
    Single comments: 19
    Multi: 49
    Blank: 28
    - Comment Stats
        (C % L): 8%
        (C % S): 15%
        (C + M % L): 30%
main.py
    LOC: 8
    LLOC: 3
    SLOC: 8
    Comments: 0
    Single comments: 0
    Multi: 0
    Blank: 0
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 0%
common\dao.py
    LOC: 202
    LLOC: 80
    SLOC: 73
    Comments: 3
    Single comments: 3
    Multi: 92
    Blank: 34
    - Comment Stats
        (C % L): 1%
        (C % S): 4%
        (C + M % L): 47%
common\__init__.py
    LOC: 14
    LLOC: 3
    SLOC: 2
    Comments: 0
    Single comments: 0
    Multi: 10
    Blank: 2
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 71%
db\info.py
    LOC: 49
    LLOC: 33
    SLOC: 32
    Comments: 0
    Single comments: 0
    Multi: 9
    Blank: 8
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 18%
db\sql_reader.py
    LOC: 114
    LLOC: 45
    SLOC: 36
    Comments: 5
    Single comments: 5
    Multi: 51
    Blank: 22
    - Comment Stats
        (C % L): 4%
        (C % S): 14%
        (C + M % L): 49%
db\__init__.py
    LOC: 17
    LLOC: 3
    SLOC: 2
    Comments: 0
    Single comments: 0
    Multi: 12
    Blank: 3
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 71%
place\business.py
    LOC: 180
    LLOC: 79
    SLOC: 77
    Comments: 2
    Single comments: 2
    Multi: 73
    Blank: 28
    - Comment Stats
        (C % L): 1%
        (C % S): 3%
        (C + M % L): 42%
place\dao.py
    LOC: 533
    LLOC: 277
    SLOC: 299
    Comments: 34
    Single comments: 34
    Multi: 115
    Blank: 85
    - Comment Stats
        (C % L): 6%
        (C % S): 11%
        (C + M % L): 28%
place\model.py
    LOC: 358
    LLOC: 162
    SLOC: 180
    Comments: 3
    Single comments: 3
    Multi: 117
    Blank: 58
    - Comment Stats
        (C % L): 1%
        (C % S): 2%
        (C + M % L): 34%
place\__init__.py
    LOC: 15
    LLOC: 3
    SLOC: 2
    Comments: 0
    Single comments: 0
    Multi: 10
    Blank: 3
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 67%
weather\business.py
    LOC: 159
    LLOC: 57
    SLOC: 76
    Comments: 10
    Single comments: 10
    Multi: 47
    Blank: 26
    - Comment Stats
        (C % L): 6%
        (C % S): 13%
        (C + M % L): 36%
weather\dao.py
    LOC: 544
    LLOC: 275
    SLOC: 304
    Comments: 39
    Single comments: 39
    Multi: 111
    Blank: 90
    - Comment Stats
        (C % L): 7%
        (C % S): 13%
        (C + M % L): 28%
weather\model.py
    LOC: 543
    LLOC: 289
    SLOC: 360
    Comments: 0
    Single comments: 0
    Multi: 107
    Blank: 76
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 20%
weather\__init__.py
    LOC: 3
    LLOC: 2
    SLOC: 2
    Comments: 0
    Single comments: 0
    Multi: 0
    Blank: 1
    - Comment Stats
        (C % L): 0%
        (C % S): 0%
        (C + M % L): 0%
** Total **
    LOC: 2966
    LLOC: 1441
    SLOC: 1584
    Comments: 115
    Single comments: 115
    Multi: 803
    Blank: 464
    - Comment Stats
        (C % L): 4%
        (C % S): 7%
        (C + M % L): 31%
```
Trong đó
* LOC (Lines of code): Tổng số dòng mã trong dự án, bao gồm cả mã, nhận xét (comments), và dòng trống (blank lines).
* LLOC (Logical lines of code): Tổng số dòng mã logic. Đây là các dòng thực sự thực hiện các lệnh trong chương trình, không bao gồm nhận xét hoặc dòng trống.
* SLOC (Source lines of code): Tổng số dòng mã nguồn. Bao gồm các dòng mã và nhận xét, nhưng không bao gồm dòng trống.
* Single comments: Tổng số dòng nhận xét đơn (các dòng nhận xét bắt đầu bằng #).
* Multi: Tổng số dòng nằm trong các khối nhận xét đa dòng (ví dụ: nhận xét trong các chuỗi ba dấu nháy """ hoặc ''' thường được sử dụng để tạo docstrings).
* Blank: Tổng số dòng trống (không chứa mã hoặc nhận xét).
* C % L: Phần trăm nhận xét trên tổng số dòng mã logic (LLOC).
* C % S: Phần trăm nhận xét trên tổng số dòng mã nguồn (SLOC).
* C + M % L: Phần trăm của các dòng nhận xét đơn và nhận xét đa dòng trên tổng số dòng mã logic (LLOC).