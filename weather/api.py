import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)

from typing import Literal

import weather.dao as weather_dao

from flask import Blueprint, jsonify, request

weather_bp = Blueprint('weather_bp', __name__)

def get_gen_weather_dao(type: Literal['MySQL', 'MongoDB'] = 'MongoDB') -> weather_dao.BasicGeneralWeatherDAO:
    if type == 'MySQL':
        return weather_dao.MySQLGeneralWeatherDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
    return weather_dao.MongoDBGeneralWeatherDAO('localhost', 27017, 'weather_vietnam')

def get_weather_status_dao(type: Literal['MySQL', 'MongoDB'] = 'MongoDB') -> weather_dao.BasicWeatherStatusDAO:
    if type == 'MySQL':
        return weather_dao.MySQLWeatherStatusDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
    return weather_dao.MongoDBWeatherStatusDAO('localhost', 27017, 'weather_vietnam')

@weather_bp.route('/weather/general_status', methods=['GET'])
def get_general_weathers():
    db_type = request.args.get('db', default='MongoDB')
    general_weather_dao = get_gen_weather_dao(db_type)
    return jsonify([general_weather.to_json() for general_weather in general_weather_dao.get_all()])

@weather_bp.route('/weather/status', methods=['GET'])
def get_weather_status():
    db_type = request.args.get('db', default='MongoDB')
    city_id = request.args.get('city_id')
    weather_status_dao = get_weather_status_dao(db_type)
    
    if city_id is None:
        return jsonify({'error': 'Required param city!'}), 400
    
    if city_id.isnumeric():
        city_id = int(city_id)
    else:
        return jsonify({'error': 'city_id is integer!'}), 400
    
    return jsonify([weather_status.to_json() for weather_status in weather_status_dao.get_all(city_id)])
    