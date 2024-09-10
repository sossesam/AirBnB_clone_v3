#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.city import City
from models.place import place_amenity
from models import storage


@app_views.route("cities/<city_id>/places", methods=["Get"], strict_slashes=False)
def get_places(city_id):
    city_ide = storage.get(City, city_id)
    if city_id == None:
         return abort(404, "Not found") 

    all_obj = storage.all(Place)
    place_list = []
    for key, value in all_obj.items():
            if value.to_dict()["city_id"] == city_id:
                place_list.append(value.to_dict())

    return jsonify(place_list), 200

@app_views.route("places/<place_id>", methods=["Get"], strict_slashes=False)
def get_place(place_id):
    place_ide = storage.get(Place, place_id)
    if place_ide == None:
         return abort(404, "Not found") 

    return jsonify(place_ide.to_dict()), 200


@app_views.route("/places/<place_id>", methods = ["DELETE"], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place:
         storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places", methods = ["POST"], strict_slashes=False)
def create_place():
    data = request.get_json()

    new_place = Place(**data)
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("places/<place_id>", methods = ["PUT"], strict_slashes=False)
def update_user(place_id):
    place = storage.get(Place, place_id)

    data = request.get_json()
    for key, value in data.items():
        if key in place.to_dict().keys():
            setattr(place, key, value)
    storage.save()

    return jsonify(place.to_dict()), 200

