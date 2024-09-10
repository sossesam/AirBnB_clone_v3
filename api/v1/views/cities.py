#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models.city import City
from models import storage


@app_views.route("states/<state_id>/cities", methods=["Get"], strict_slashes=False)
def get_cities(state_id):
    city_obj = storage.all(City)
    state_city = []
    for city in city_obj.values():
        if city.state_id == state_id:
            state_city.append(city.to_dict())
        
    return jsonify(state_city), 200

@app_views.route("/cities/<city_id>", methods=["Get"], strict_slashes=False)
def get_cities_by_id(city_id):
    city_obj = storage.get(City, city_id)
    if city_obj:
            return jsonify(city_obj.to_dict())
    return abort(404, "Not Found")

@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_cities_by_id(city_id):
    city_obj = storage.get(City, city_id)
    if city_obj:
            storage.delete(city_obj)
            return jsonify({}), 200
    return abort(404, "Not found")

@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_cities(state_id):
    state_obj = storage.get(State, state_id)
    if state_obj is None:
         return abort(404, "Not Found")

    data = request.get_json()

    city = City()
    city.name = data["name"]
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 200


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_cities(city_id):
    if request.mimetype != "application/json":
         return abort(400, "Not a json")
    
    city_obj = storage.get(City, city_id)
    if city_obj is None:
         return abort(404, "Not Found")
    
    data = request.get_json()
    
    for key, value in data.items():
         if key in city_obj.to_dict().keys():
              setattr(city_obj, key, value)
         
    
    storage.new(city_obj)
    storage.save()
    return jsonify(city_obj.to_dict()), 200
        

