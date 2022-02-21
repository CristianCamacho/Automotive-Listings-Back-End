from flask import Blueprint, json, request, jsonify
from resources.cache import cache
from playhouse.shortcuts import model_to_dict
import models
import requests
import xmltodict
from datetime import date

listings = Blueprint('listings', 'listings')


@listings.route('get_listings', methods=['GET'])
def get_listings():
    listings_dict = []

    try:
        for listing in models.Listings.select():
            listings_dict.append(model_to_dict(listing))
        return jsonify(
            listings=listings_dict,
            result='success'
        ), 200
    except:
        return jsonify(
            message='Could not retreive listings.'
        ), 204
    
@listings.route('get_listing_by_id', methods=['GET'])
def get_listing_by_id():
    try:
        listing_dict=model_to_dict(models.Listings.get(models.Listings.id == request.args.get('id')))
        return jsonify(
            listing=listing_dict,
            message='Successfully retrieved listing.'
        ), 200
    except:
        return jsonify(
            message='Could not retreive listing.'
        ), 204


@listings.route('create_listing', methods=['POST'])
def create_listing():
    payload = request.get_json()

    try:
        r = requests.get('https://www.fueleconomy.gov/ws/rest/vehicle/%s' % (payload['govid']))

        dict_from_xml_vehicle = xmltodict.parse(r.content)
        created_listing = models.Listings.create(
            gov_vehicle_id=payload['govid'],
            mileage=payload['mileage'],
            zipcode=payload['zipcode'],
            vin=payload['vin'],
            price=payload['price'],
            lien=payload['lien'],
            create_date=date.today(),
            year=dict_from_xml_vehicle['vehicle']['year'],
            make=dict_from_xml_vehicle['vehicle']['make'],
            model=dict_from_xml_vehicle['vehicle']['model'],
            fuel=dict_from_xml_vehicle['vehicle']['fuelType'],
            city=dict_from_xml_vehicle['vehicle']['city08'],
            highway=dict_from_xml_vehicle['vehicle']['highway08'],
            trans=dict_from_xml_vehicle['vehicle']['trany'],
            cylinders=dict_from_xml_vehicle['vehicle']['cylinders'],
            drive=dict_from_xml_vehicle['vehicle']['drive']
        )
        return jsonify(
            data=model_to_dict(created_listing),
            message='Created listing.',
            status=201
        ), 201
    except:
        return jsonify(
            message='Failed to create listing.',
            status=400
        ), 400
