#!/usr/bin/python3
""" Places routes handler """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import city
from models import place
from models import user
from models import state
from api.v1.views.cities import do_get_cities
from api.v1.views.places_amenities import do_get_amenities
import json


def do_check_id(cls, place_id):
    """
        If the place_id is not linked to any Place object, raise a 404 error
    """
    try:
        get_place = storage.get(cls, place_id)
        get_place.to_dict()
    except Exception:
        abort(404)
    return get_place


def do_get_places(city_id, place_id):
    """
       Retrieves the list of all Place objects
       if place_id is not none get a Place object
    """
    if (place_id is not None):
        get_place = do_check_id(place.Place, place_id).to_dict()
        return jsonify(get_place)
    my_city = storage.get(city.City, city_id)
    try:
        all_places = my_city.places
    except Exception:
        abort(404)
    places = []
    for c in all_places:
        places.append(c.to_dict())
    return jsonify(places)


def do_delete_place(place_id):
    """
        Deletes a Place object
        Return: an empty dictionary with the status code 200
    """
    get_place = do_check_id(place.Place, place_id)
    storage.delete(get_place)
    storage.save()
    response = {}
    return jsonify(response)


def do_create_place(request, city_id):
    """
        Creates a place object
        Return: new place object
    """
    do_check_id(city.City, city_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    try:
        user_id = body_request['user_id']
    except KeyError:
        abort(400, 'Missing user_id')
    do_check_id(user.User, user_id)
    try:
        place_name = body_request['name']
    except KeyError:
        abort(400, 'Missing name')
    new_place = place.Place(name=place_name, city_id=city_id, user_id=user_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict())


def do_update_place(place_id, request):
    """
        Updates a Place object
    """
    get_place = do_check_id(place.Place, place_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    for k, v in body_request.items():
        if (k not in ('id', 'created_at', 'updated_at')):
            setattr(get_place, k, v)
    storage.save()
    return jsonify(get_place.to_dict())


def do_search(request):
    """
    retrieves all Place objects depending of the JSON
    in the body of the request
    """
    body_request = request.get_json()
    if body_request is None:
        abort(400, 'Not a JSON')
    places_list = []
    places_amenity_list = []
    all_cities = []
    states = body_request.get('states')
    cities = body_request.get('cities')
    amenities = body_request.get('amenities')
    if len(body_request) == 0 or (states is None and cities is None):
        places = storage.all(place.Place)
        for p in places.values():
            places_list.append(p.to_dict())
    if states is not None and len(states) is not 0:
        for id in states:
            get_cities = do_get_cities(id, None).json
            for city in get_cities:
                all_cities.append(city.get('id'))
        for id in all_cities:
            places = do_get_places(id, None)
            for p in places.json:
                places_list.append(p)
    if cities is not None and len(cities) is not 0:
        for id in cities:
            places = do_get_places(id, None)
            for p in places.json:
                places_list.append(p)
    if amenities is not None:
        if (len(amenities) is 0):
            return jsonify({})
        for p in places_list:
            place_id = p.get('id')
            get_amenities = do_get_amenities(place_id).json
            for a in get_amenities:
                amenity_id = a.get('id')
                if(amenity_id in amenities):
                    if p not in places_amenity_list:
                        places_amenity_list.append(p)
        return jsonify(places_amenity_list)
    return jsonify(places_list)


@app_views.route('/cities/<city_id>/places/', methods=['GET', 'POST'],
                 defaults={'place_id': None}, strict_slashes=False)
@app_views.route('/places/<place_id>', defaults={'city_id': None},
                 methods=['GET', 'DELETE', 'PUT'])
def places(city_id, place_id):
    """
        Handle places requests with needed functions
    """
    if (request.method == "GET"):
        return do_get_places(city_id, place_id)
    elif (request.method == "DELETE"):
        return do_delete_place(place_id)
    elif (request.method == "POST"):
        return do_create_place(request, city_id), 201
    elif (request.method == "PUT"):
        return do_update_place(place_id, request), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
    retrieves all Place objects depending of the JSON
    in the body of the request
    """
    return do_search(request)
