#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route("/states", methods=["Get"], strict_slashes=False)
def get_states():
    all_obj = storage.all(State)
    state_list = []
    for key, value in all_obj.items():
            state_list.append(value.to_dict())

    return jsonify(state_list)

@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state_id(state_id):
    all_obj = storage.get(State)
    if all_obj:
        return jsonify(all_obj)
            
    return jsonify({"error":"not found"}), 404
            
@app_views.delete("/states/<state_id>", strict_slashes=False)
def delete_state_id(state_id):
    selected_state = storage.get(State, state_id)
    if selected_state:
        storage.delete(selected_state)
        storage.save()
    else:
          abort(404) 
    return jsonify({}), 200

@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_states():
    if request.mimetype != "application/json":
         return abort(400, "Not a json")
    
    data = request.get_json()
    if "name" not in data:
         return abort(400, "Name missing")

    newstate = State()
    newstate.name = data["name"]

    storage.new(newstate)
    storage.save()

    return jsonify(newstate.to_dict()), 200
        
@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_states(state_id):
    if request.mimetype != "application/json":
         return abort(400, "Not a json")
    
    data = request.get_json()
    if "name" not in data:
         return abort(400, "Name missing")
    
    state_obj = storage.get(State, state_id)
    
    for key, value in data.items():
         if key in state_obj.to_dict().keys():
              setattr(state_obj, key, value)
    storage.save()

    return jsonify(state_obj.to_dict()), 200
    
            
            





    