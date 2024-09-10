#!/usr/bin/python3
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.register_blueprint(app_views)

@app.teardown_appcontext
def tear_down_engine(exception):
    storage.close

@app.errorhandler(404)
def error_message(error):
    data = {"error":"Not Found"}

    return jsonify(data),404



if __name__ == "__main__":
    HOST = os.getenv("HBNB_API_HOST","0.0.0.0")
    PORT = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST,port=PORT, threaded=True)