from flask import Blueprint, json, request, jsonify
import requests
from resources.cache import cache
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from datetime import datetime
import xmltodict 
auto_info = Blueprint('auto_info', 'auto_info')

session = FuturesSession()

@auto_info.route('/get_years', methods=['GET'])
@cache.cached(timeout=86400)
def get_years():
    r = requests.get('https://www.fueleconomy.gov/ws/rest/vehicle/menu/year')
    dict_from_xml_years = xmltodict.parse(r.content)

    list_of_years = []
    for item in dict_from_xml_years['menuItems']['menuItem']:
        list_of_years.append(item['value'])

    return jsonify(
        years=list_of_years
    ), 200