#!/usr/bin/python3
""" Generates routes for Blueprint app_views """

from flask import Flask
from flask import Blueprint
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """ Return first simple json for route /status """
    my_dict = {"status": "OK"}
    return jsonify(my_dict)


@app_views.route('/stats')
def stats():
    """ Endpoint that retrieves the number of each objects by type """
    return jsonify({"amenities": storage.count(Amenity),
                    "cities": storage.count(City),
                    "places": storage.count(Place),
                    "reviews": storage.count(Review),
                    "states": storage.count(State),
                    "users": storage.count(User)})
