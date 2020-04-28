from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.teardown_appcontext
def teardown(exception):
    """teardown"""
    storage.close()

    
if __name__ == "__main__":
    host_api = getenv("HBNB_API_HOST", "0.0.0.0")
    port_api = getenv("HBNB_API_PORT", "5000")
    app.run(host=host_api, port=port_api, threaded=True)
