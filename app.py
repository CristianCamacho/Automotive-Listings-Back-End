from flask import Flask, json, request, jsonify, after_this_request
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

CORS(app, resources={r"/*": {"origins": os.environ.get('FRONT_END')}}, supports_credentials=True)

@app.route('/')
def ping():
    return jsonify(
        message='ping'
    ), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)