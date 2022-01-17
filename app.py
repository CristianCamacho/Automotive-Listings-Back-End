from flask import Flask, json, request, jsonify

app = Flask(__name__)

@app.route('/')
def ping():
    return jsonify(
        message='ping'
    ), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)