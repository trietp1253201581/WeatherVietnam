import datetime as dt
import requests

api_key = "e74a2bf1acc6defe706eee2ae95698c9"

city_names = ["Son La", "Tuyen Quang", "Ha Noi", "Thanh Hoa", "Vinh", "Da Nang", "Da Lat", "Can Tho", "Ho Chi Minh"]
country_code = "VN"
responses = []

for city_name in city_names:
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    url = f"{base_url}?q={city_name},{country_code}&limit=1&appid={api_key}"
    response = requests.get(url).json()[0]
    city_lat = response['lat']
    city_lon = response['lon']
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    url = f"{base_url}?lat={city_lat}&lon={city_lon}&appid={api_key}"
    response = requests.get(url).json()
    responses.append(response)

print(responses[0])