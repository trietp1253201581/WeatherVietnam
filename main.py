import datetime as dt
import requests

def weather():
    api_key = "e74a2bf1acc6defe706eee2ae95698c9"
    city_names = ["Son La", "Tuyen Quang"]
    country_code = "VN"
    responses = []
    responses_aqi = []

    for city_name in city_names:
        base_url = "http://api.openweathermap.org/geo/1.0/direct"
        url = f"{base_url}?q={city_name},{country_code}&limit=1&appid={api_key}"
        response = requests.get(url).json()[0]
        city_lat = response['lat']
        city_lon = response['lon']
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': city_lat,
            'lon': city_lon,
            'appid': api_key
        }
        response = requests.get(base_url, params=params).json()
        responses.append(response)
        if 'rain' in response:
            print(f"{response['name']} has rain!")
        base_url = "https://api.openweathermap.org/data/2.5/air_pollution"
        response = requests.get(base_url, params=params).json()
        responses_aqi.append(response)

    print(responses)
    print('AQI::', responses_aqi)
    
if __name__ == '__main__':
    weather()
