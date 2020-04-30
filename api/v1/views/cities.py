#!/usr/bin/python3
""" Cities routes handler """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import state
from models import city


def do_check_id(cls, city_id):
    """
        If the city_id is not linked to any City object, raise a 404 error
    """
    try:
        get_city = storage.get(cls, city_id)
        get_city.to_dict()
    except Exception:
        abort(404)
    return get_city


def do_get_cities(state_id, city_id):
    """
       Retrieves the list of all City objects
       if city_id is not none get a City object
    """
    if (city_id is not None):
        get_city = do_check_id(city.City, city_id).to_dict()
        return jsonify(get_city)
    my_state = storage.get(state.State, state_id)
    try:
        all_cities = my_state.cities
    except Exception:
        abort(404)
    cities = []
    for c in all_cities:
        cities.append(c.to_dict())
    return jsonify(cities)


def do_delete_city(city_id):
    """
        Deletes a City object
        Return: an empty dictionary with the status code 200
    """
    get_city = do_check_id(city.City, city_id)
    storage.delete(get_city)
    storage.save()
    response = {}
    return jsonify(response)


def do_create_city(request, state_id):
    """
        Creates a city object
        Return: new city object
    """
    do_check_id(state.State, state_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    try:
        city_name = body_request['name']
    except KeyError:
        abort(400, 'Missing name')
    new_city = city.City(name=city_name, state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict())


def do_update_city(city_id, request):
    """
        Updates a City object
    """
    get_city = do_check_id(city.City, city_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    for k, v in body_request.items():
        if (k not in ('id', 'created_at', 'updated_at')):
            setattr(get_city, k, v)
    storage.save()
    return jsonify(get_city.to_dict())


@app_views.route('/states/<state_id>/cities/', methods=['GET', 'POST'],
                 defaults={'city_id': None}, strict_slashes=False)
@app_views.route('/cities/<city_id>', defaults={'state_id': None},
                 methods=['GET', 'DELETE', 'PUT'])
def cities(state_id, city_id):
    """
        Handle cities requests with needed functions
    """
    if (request.method == "GET"):
        return do_get_cities(state_id, city_id)
    elif (request.method == "DELETE"):
        return do_delete_city(city_id)
    elif (request.method == "POST"):
        return do_create_city(request, state_id), 201
    elif (request.method == "PUT"):
        return do_update_city(city_id, request), 200
