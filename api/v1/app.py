#!/usr/bin/python3
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
"""
My first API
"""

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_storage(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_404(e):
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    host_api = getenv("HBNB_API_HOST", "0.0.0.0")
    port_api = getenv("HBNB_API_PORT", "5000")
    app.run(host=host_api, port=port_api, threaded=True)
