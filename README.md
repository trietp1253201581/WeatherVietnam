# WeatherVietnam
## Các thư viện được sử dụng
Có thể cần cài đặt các thư viện logging, typing, json, requests, schedule, mysql-connector, pymongo, Flask, matplotlib. Các thư viện cần cài đặt có trong [requirements.txt](requirements.txt)
```bash
pip install -r requirements.txt
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
* `db`: Các khởi tạo và thông tin liên quan tới dữ liệu
  * [config.py](db/config.py)
  * [sql_reader.py](db/sql_reader.py)

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
Đánh giá xem trong [radon_review.md](radon_review.md)