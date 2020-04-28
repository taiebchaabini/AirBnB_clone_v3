from flask import Blueprint
"""
Blueprint for app views with url prefix to /api/v1
"""
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
