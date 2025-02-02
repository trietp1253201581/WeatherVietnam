import json
import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)
from typing import Literal, Dict, List
from model import City
from dao import BasicCityDAO, BasicCountryDAO, MySQLCityDAO, MySQLCountryDAO
import requests

config_dir = os.path.join(init_dir, 'config.json')
with open(config_dir, 'r') as config_file:
    config = json.load(config_file)

def _get_coord_from_api(city: City,
                        api: Literal['OPEN_WEATHER_MAP'] = 'OPEN_WEATHER_MAP') -> tuple[float, float]:
    if api == 'OPEN_WEATHER_MAP':
        api_key = config['OPEN_WEATHER_MAP_API_KEY']
    else:
        raise ValueError('Not supported API!')
    
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    url = f"{base_url}?q={city.name},{city.country.code}&limit=1&appid={api_key}"
    response = requests.get(url).json()[0]
    return response['lon'], response['lat']

def _get_city(city: int|str,
              city_dao: BasicCityDAO) -> City:
    if isinstance(city, int):
        result_city = city_dao.get(city_id=city)
    else:
        result_city = city_dao.get(city_name=city)
    if result_city.lon is None or result_city.lat is None:
        result_city.lon, result_city.lat = _get_coord_from_api(result_city)
        city_dao.insert(result_city)
    return result_city

def _get_all_of_country(country: str,
                        city_dao: BasicCityDAO) -> list[City]:
    citys = city_dao.get_all(country_code=country)
    for result_city in citys:
        if result_city.lon is None or result_city.lat is None:
            result_city.lon, result_city.lat = _get_coord_from_api(result_city)
            city_dao.insert(result_city)
    return citys

def get_city(city_dao: BasicCityDAO, 
             type: Literal['list_country', 'all_country', 'one_city'] = 'one_city',
             city: int|str|None = None,
             country: str|list[str]|None = None):
    
    if type == 'one_city' and city is not None:
        return _get_city(city, city_dao)
    elif type == 'all_country' and isinstance(country, str):
        return _get_all_of_country(country, city_dao)
    elif type == 'list_country' and isinstance(country, list):
        results_city_dict: Dict[str, list[City]] = {}
        for one_country in country:
            results_city_dict[one_country] = _get_all_of_country(country)
        return results_city_dict
    else:
        return None
    
def insert_city(city_dao: BasicCityDAO,
                new_city: City|list[City]) -> None:
    if isinstance(new_city, City):
        new_citys = [new_city]
    else:
        new_citys = new_city

    for city in new_citys:
        city_dao.insert(city)
        
def delete_city(city_dao: BasicCityDAO,
                city: City|int|list[City|int]) -> None:
    if isinstance(city, City):
        city_ids = [city.city_id]
    elif isinstance(city, int):
        city_ids = [city]
    else:
        city_ids: List[int] = []
        for city_item in city:
            if isinstance(city_item, City):
                city_ids.append(city_item.city_id)
            else:
                city_ids.append(city_item)
    
    for city_id in city_ids:
        city_dao.delete(city_id) 
        
def get_country(country_code: str,
                country_dao: BasicCountryDAO):
    return country_dao.get(country_code)
            
if __name__ == '__main__':
    city_dao = MySQLCityDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
    for city in get_city(city_dao ,'all_country', country='VN'):
        print(city)