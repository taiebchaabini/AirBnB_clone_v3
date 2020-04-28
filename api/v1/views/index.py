from models import storage
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """ return status"""
    my_dict = {"status": "OK"}
    return jsonify(my_dict)

@app_views.route('/stats')
def stats():
    """return stats"""
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
