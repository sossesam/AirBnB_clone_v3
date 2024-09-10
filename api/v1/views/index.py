#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route("/status")
def check_status():
    data = {"status":"OK"}
    return jsonify(data)

@app_views.route("stats")
def api_count():
    all_obj = storage.all()
    new_obj = {}
    for key, value in all_obj.items():
        new_obj[value.__class__.__name__] = storage.count(value.__class__)
    return jsonify(new_obj)


