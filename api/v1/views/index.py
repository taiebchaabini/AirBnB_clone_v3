from models import storage
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status/')
def status():
    """ return status"""
    my_dict = {"status": "OK"}
    return jsonify(my_dict)
