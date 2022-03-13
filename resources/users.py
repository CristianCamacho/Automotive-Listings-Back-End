from flask import Blueprint, json, request, jsonify
from playhouse.shortcuts import model_to_dict
import models

users = Blueprint('users', 'users')

@users.route('create_user', methods=['POST'])
def create_user():
    payload = request.get_json()
    print(payload['password'])
    # try:
    models.Users.create(
        username=payload['username'],
        password=payload['password']
    )
    return jsonify(
        message='Successfully created user.'
    ), 201
    # except:
    #     return jsonify(
    #         message='Unable to create user.'
    #     ), 400

@users.route('get_user_by_id', methods=['GET'])
def get_user_by_id():
    try:
        users_dict=model_to_dict(models.Users.get(models.Users.id == request.args.get('id')))
        return jsonify(
            users=users_dict,
            message='Successfully retrieved Users.'
        ), 200
    except:
        return jsonify(
            message='Could not retreive Users.'
        ), 204