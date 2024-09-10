#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False)
def get_amenities():
    amenities = storage.all(Amenity)
    list_amenities = []
    for key, value in amenities.items():
        list_amenities.append(value.to_dict())
        
    return jsonify(list_amenities)

@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenities_by_id(amenity_id):
    amenities = storage.get(Amenity, amenity_id) 
    if amenities:  
        return jsonify(amenities.to_dict())
    else:
        return abort(404, "Not Found")
    

@app_views.route("/amenities/<amenity_id>", methods = ["DELETE"], strict_slashes=False)
def delete_amenities(amenity_id):
    amenities = storage.get(Amenity, amenity_id) 
    if amenities:  
        amenities.delete()
    else:
        return abort(404, "Not Found")
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods = ["POST"], strict_slashes=False)
def create_amenity():
    data = request.get_json()

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201

@app_views.route("/amenities/<amenity_id>", methods = ["PUT"], strict_slashes=False)
def update_amenities(amenity_id):
    amenity = storage.get(Amenity, amenity_id)

    data = request.get_json()
    for key, value in data.items():
        if key in amenity.to_dict().keys():
            setattr(amenity, key, value)
    storage.save()

    return jsonify(amenity.to_dict())
