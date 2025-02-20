import os
init_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import sys
sys.path.append(init_dir)

from typing import Literal

from place.dao import BasicCityDAO, MySQLCityDAO, MongoDBCityDAO
from common.dao import NotExistDataException, DAOException

from flask import Blueprint, jsonify, request

def get_dao(type: Literal['MySQL', 'MongoDB'] = 'MongoDB') -> BasicCityDAO:
    if type == 'MySQL':
        return MySQLCityDAO('localhost', 'weather_vietnam', 'root', 'Asensio1234@')
    return MongoDBCityDAO('localhost', 27017, 'weather_vietnam')

place_bp = Blueprint('place_bp', __name__)


@place_bp.route('/cities', methods=['GET'])
def get_cities():
    db_type = request.args.get('db', default='MongoDB')
    country_code = request.args.get('country', default='VN')
    dao = get_dao(db_type)
    return jsonify([city.to_json() for city in dao.get_all(country_code)])

@place_bp.route('/city', methods=['GET'])
def get_city():
    db_type = request.args.get('db', default='MongoDB')
    city_id = request.args.get('id')
    city_name = request.args.get('name')
    dao = get_dao(db_type)
    
    if city_id is None and city_name is None:
        return jsonify({'error': 'Required parameter for city id or name!'}), 400
    if city_id is not None:
        if city_id.isnumeric():
            city_id = int(city_id)
        else:
            return jsonify({'error': 'Required parameter for city id is integer!'}), 400
    
    try:
        city = dao.get(city_id, city_name)
        return jsonify(city.to_json())
    except NotExistDataException:
        return jsonify({'error': 'City not found!'}), 404
    except DAOException:
        return jsonify({'error': 'Database not access!'}), 400