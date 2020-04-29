#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
"""
Generates routes for Blueprint app_views
"""


@app_views.route('/status')
def status():
    """
    Return first simple json for route /status
    """
    my_dict = {'status': "OK"}
    return jsonify(my_dict)


@app_views.route('/stats')
def stats():
    """
    endpoint that retrieves the number of each objects by type
    """
    """return stats"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
