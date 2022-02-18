from importlib import resources
from flask import Flask, json, request, jsonify, after_this_request
from flask_cors import CORS
from dotenv import load_dotenv
from resources.auto_info import auto_info
from resources.listings import listings
from resources.cache import cache
from flask_caching import Cache
import os
import models

load_dotenv()

config = {
    "DEBUG": True,        
    "CACHE_TYPE": "SimpleCache",  
    "CACHE_DEFAULT_TIMEOUT": 300
}

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

app.config.from_mapping(config)
cache.init_app(app)

CORS(app, resources={r"/*": {"origins": os.environ.get('FRONT_END')}}, supports_credentials=True)

app.register_blueprint(auto_info, url_prefix='/api/v1/auto_info')
app.register_blueprint(listings, url_prefix='/api/v1/listings')

@app.before_request
def before_request():
    print("you should see this before each request") 
    models.DATABASE.connect()

    @after_this_request 
    def after_request(response):
        print("you should see this after each request") 
        models.DATABASE.close()
        return response 

@app.route('/')
def ping():
    return jsonify(
        message='ping'
    ), 200

if __name__ == "__main__":
    models.initialize()
    app.run(debug=True, port=5000)