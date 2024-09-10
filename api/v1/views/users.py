#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
from models import storage

@app_views.route("/users", methods=["Get"], strict_slashes=False)
def get_users():
    all_obj = storage.all(User)
    user_list = []
    for key, value in all_obj.items():
            user_list.append(value.to_dict())

    return jsonify(user_list), 200

@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user_id(user_id):
    all_obj = storage.get(User, user_id)
    if all_obj:
         return jsonify(all_obj.to_dict())
            
    return jsonify({"error":"not found"}), 404

@app_views.route("/users/<user_id>", methods = ["DELETE"], strict_slashes=False)
def delete_user(user_id):
    users = storage.get(User, user_id) 
    if users:  
        users.delete()
    else:
        return abort(404, "Not Found")
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods = ["POST"], strict_slashes=False)
def create_user():
    data = request.get_json()

    new_user = User(**data)
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201

@app_views.route("/users/<user_id>", methods = ["PUT"], strict_slashes=False)
def update_users(user_id):
    user = storage.get(User, user_id)

    data = request.get_json()
    for key, value in data.items():
        if key in user.to_dict().keys():
            setattr(user, key, value)
    storage.save()

    return jsonify(user.to_dict())
