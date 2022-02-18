from flask import Blueprint, json, request, jsonify
from resources.cache import cache
from playhouse.shortcuts import model_to_dict
import models
from datetime import date

listings = Blueprint('listings', 'listings')

@listings.route('get_listings', methods=['GET'])
def get_listings():
    return jsonify(
        result='success'
    ), 200

@listings.route('create_listing', methods=['POST'])
def create_listing():
    payload = request.get_json()

    try:
        created_listing = models.Listings.create(
            gov_vehicle_id = payload['govid'],
            create_date=date.today()
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