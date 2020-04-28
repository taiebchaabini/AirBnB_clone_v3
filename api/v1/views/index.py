from api.v1.views import app_views
from flask import jsonify
"""
Generates routes for Blueprint app_views
"""


@app_views.route('/status')
def status():
    """
    Return first simple json for route /status
    """
    my_dict = {'status': "OK"}
    return (jsonify(my_dict))
