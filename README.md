# WeatherVietnam
## Dữ liệu
Dữ liệu về thời tiết của các thành phố ở Việt Nam được lấy từ API của OpenWeatherMap.

Dữ liệu gốc là một JSON Object, được lấy từ API của OpenWeatherMap có dạng sau:

`https://api.openweathermap.org/data/2.5/weather?lat=...&lon=...&apiid=api_key`

trong đó lat, lon là tọa độ của thành phố cần lấy.

Để lấy lat và lon của một thành phố, dùng api

`http://api.openweathermap.org/geo/1.0/direct?q=..country_code..,..city_name..,&limit=1&appid=api_key`

trong đó country_code là Code của quốc gia theo ISO 3166-1 alpha-2, city name là tên viết cách không dấu của tỉnh/thành phố.

Chi tiết về dữ liệu xem ở file [db_info.md](db/db_info.md)

API Key của tôi được lưu giữ trong `config.json`, được ẩn đi để tăng tính bảo mật (thêm vào .gitignore).
