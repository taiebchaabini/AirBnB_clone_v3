#!/usr/bin/python3
""" Places amenities routes handler """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import place
from models import amenity


def do_check_id(cls, amenity_id):
    """
        If the amenity_id is not linked to any Amenity object, raise a 404 error
    """
    try:
        get_amenity = storage.get(cls, amenity_id)
        get_amenity.to_dict()
    except Exception:
        abort(404)
    return get_amenity


def do_get_amenities(place_id):
    """
       Retrieves the list of all Amenity objects
       if amenity_id is not none get a Amenity object
    """
    do_check_id(place.Place, place_id)
    my_place = storage.get(place.Place, place_id)
    try:
        all_amenities = my_place.amenities
    except Exception:
        abort(404)
    amenities = []
    for c in all_amenities:
        amenities.append(c.to_dict())
    return jsonify(amenities)


def do_delete_amenity(place_id, amenity_id):
    """
        Deletes a Amenity object
        Return: an empty dictionary with the status code 200
    """
    do_check_id(place.Place, place_id)
    get_amenity = do_check_id(amenity.Amenity, amenity_id)
    if (get_amenity.place_id != place_id):
        abort(404)
    storage.delete(get_amenity)
    storage.save()
    response = {}
    return jsonify(response), 200


def do_create_amenity(place_id, amenity_id):
    """
        Links a amenity object
        Return: linked amenity object
    """
    do_check_id(place.Place, place_id)
    get_amenity = do_check_id(amenity.Amenity, amenity_id)
    if (get_amenity.place_id == place_id):
        return jsonify(get_amenity.to_dict()), 200
    get_amenity.place_id = place_id
    storage.save()
    return jsonify(get_amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/', methods=['GET'],
                 strict_slashes=False)
@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST', 'DELETE'],
                 strict_slashes=False)
def amenities(place_id, amenity_id):
    """
        Handle amenities requests with needed functions
    """
    if (request.method == "GET"):
        return do_get_amenities(place_id)
    elif (request.method == "DELETE"):
        return do_delete_amenity(place_id, amenity_id)
    elif (request.method == "POST"):
        return do_create_amenity(place_id, amenity_id)
