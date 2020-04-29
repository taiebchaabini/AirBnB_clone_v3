from flask import Blueprint
"""
Blueprint for app views with url prefix to /api/v1
"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views import states, \
    cities, amenities, users, places, places_reviews
