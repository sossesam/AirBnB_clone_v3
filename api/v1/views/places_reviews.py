#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.place import Place
from models.review import  Review
from models import storage


@app_views.route("places/<place_id>/reviews", methods=["Get"], strict_slashes=False)
def get_place_review(place_id):
    city_ide = storage.get(Place, place_id)
    if place_id == None:
         return abort(404, "Not found") 

    all_obj = storage.all(Review)
    review_list = []
    for key, value in all_obj.items():
            if value.to_dict()["place_id"] == place_id:
                review_list.append(value.to_dict())

    return jsonify(review_list), 200


@app_views.route("reviews/<review_id>", methods=["Get"], strict_slashes=False)
def get_review(review_id):
    review_obj = storage.get(Review, review_id)
    if review_obj == None:
         return abort(404, "Not found") 

    return jsonify(review_obj.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods = ["DELETE"], strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if review:
         storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("places/<place_id>/reviews", methods = ["POST"], strict_slashes=False)
def create_review():
    data = request.get_json()

    new_review = Review(**data)
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("reviews/<review_id>", methods = ["PUT"], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)

    data = request.get_json()
    for key, value in data.items():
        if key in review.to_dict().keys():
            setattr(review, key, value)
    storage.save()

    return jsonify(review.to_dict()), 200
