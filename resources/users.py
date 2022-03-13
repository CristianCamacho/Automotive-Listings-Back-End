from flask import Blueprint, json, request, jsonify
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, current_user, logout_user
import models

users = Blueprint('users', 'users')

@users.route('create_user', methods=['POST'])
def create_user():
    payload = request.get_json()
    try:
        models.Users.get(models.Users.username == payload['username'])
    except models.DoesNotExist:
        try:
            password_hash = generate_password_hash(payload['password'])
            models.Users.create(
                username=payload['username'],
                password=password_hash
            )
            return jsonify(
                message='Successfully created user.'
            ), 201
        except:
            return jsonify(
                message='Unable to create user.'
            ), 400
    return jsonify(
        message='Unable to create user.'
    ), 400


@users.route('login', methods=['POST'])
def login():
    payload = request.get_json()
    try:
        user = models.Users.get(models.Users.username == payload['username'])
        user_dict = model_to_dict(user)

        if check_password_hash(user_dict['password'], payload['password']):
            login_user(user, remember=True)
            user_dict = model_to_dict(current_user)
            user_dict.pop('password')

            return jsonify(
                user=user_dict,
                message=f"Successfully logged in {user_dict['username']}",
                status=202
            ), 202
        else:
            return jsonify(
                message='Invalid credentials. pass'
            ), 401
    except:
        return jsonify(
            message='Invalid credentials. user'
        ), 401

@users.route('get_user_by_id', methods=['GET'])
def get_user_by_id():
    try:
        users_dict = model_to_dict(models.Users.get(
            models.Users.id == request.args.get('id')))
        return jsonify(
            users=users_dict,
            message='Successfully retrieved Users.'
        ), 200
    except:
        return jsonify(
            message='Could not retreive Users.'
        ), 204

@users.route('logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify(
        message='User logged out.'
    ), 200

@users.route('get_current_user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify(
        user=current_user.username
    ), 200