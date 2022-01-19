from flask import Blueprint, json, request, jsonify
import requests
from resources.cache import cache
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
from datetime import datetime

auto_info = Blueprint('auto_info', 'auto_info')

@auto_info.route('/get_years', methods=['GET'])
@cache.cached(timeout=70)
def get_years():
    now = datetime.now()
    return jsonify(
        message=now
    )