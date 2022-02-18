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


@auto_info.route('/get_makes', methods=['GET'])
@cache.cached(timeout=86400, query_string=True)
def get_makes():
    r = requests.get('https://www.fueleconomy.gov/ws/rest/vehicle/menu/make?year=%s' % (request.args.get('year')))

    dict_from_xml_makes = xmltodict.parse(r.content)
    list_of_makes = []

    for item in dict_from_xml_makes['menuItems']['menuItem']:
        list_of_makes.append(item['value'])

    return jsonify(
        makes=list_of_makes
    ), 200

@auto_info.route('/get_models', methods=['GET'])
@cache.cached(timeout=86400, query_string=True)
def get_models():
    r = requests.get('https://www.fueleconomy.gov/ws/rest/vehicle/menu/model?year=%s&make=%s' % (request.args.get('year'), (request.args.get('make'))))
    
    dict_from_xml_models = xmltodict.parse(r.content)
    list_of_models = []

    for item in dict_from_xml_models['menuItems']['menuItem']:
        list_of_models.append(item['value'])

    return jsonify(
        models=list_of_models
    ), 200

@auto_info.route('/get_options', methods=['GET'])
@cache.cached(timeout=86400, query_string=True)
def get_options():
    r = requests.get('https://www.fueleconomy.gov/ws/rest/vehicle/menu/options?year=%s&make=%s&model=%s' % (request.args.get('year'), request.args.get('make'), request.args.get('model')))
    
    dict_from_xml_options = xmltodict.parse(r.content)
    list_of_options = []

    for item in dict_from_xml_options['menuItems']['menuItem']:
        list_of_options.append(item['text'])

    return jsonify(
        options=list_of_options
    ), 200

@auto_info.route('/get_auto_info_by_govid', methods=['GET'])
@cache.cached(timeout=86400, query_string=True)
def get_by_govid():
    r = requests.get('https://www.fueleconomy.gov/ws/rest/vehicle/%s' % (request.args.get('id')))

    dict_from_xml_vehicle = xmltodict.parse(r.content)

    return jsonify(
        year=dict_from_xml_vehicle['vehicle']['year'],
        make=dict_from_xml_vehicle['vehicle']['make'],
        model=dict_from_xml_vehicle['vehicle']['model'],
        fuel=dict_from_xml_vehicle['vehicle']['fuelType'],
        city=dict_from_xml_vehicle['vehicle']['city08'],
        highway=dict_from_xml_vehicle['vehicle']['highway08'],
        trans=dict_from_xml_vehicle['vehicle']['trany'],
        cylinders=dict_from_xml_vehicle['vehicle']['cylinders'],
        drive=dict_from_xml_vehicle['vehicle']['drive']
        
    ), 200