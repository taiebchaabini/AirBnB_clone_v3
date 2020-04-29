from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import amenity


def do_check_id(amenity_id):
    """
        If the amenity_id is not linked to
        any Amenity object, raise a 404 error
    """
    try:
        get_amenity = storage.get(amenity.Amenity, amenity_id)
        get_amenity.to_dict()
    except Exception:
        abort(404)
    return get_amenity


def do_get_amenities(amenity_id):
    """
       Retrieves the list of all Amenity objects
       if amenity_id is not none get a Amenity object
    """
    if (amenity_id is not None):
        get_amenity = do_check_id(amenity_id).to_dict()
        return jsonify(get_amenity)
    all_amenities = storage.all(amenity.Amenity)
    amenities = []
    for v in all_amenities.values():
        amenities.append(v.to_dict())
    return jsonify(amenities)


def do_delete_amenity(amenity_id):
    """
        Deletes a Amenity object
        Return: an empty dictionary with the status code 200
    """
    get_amenity = do_check_id(amenity_id)
    storage.delete(get_amenity)
    storage.save()
    response = {}
    return jsonify(response)


def do_create_amenity(request):
    """
        Creates a amenity object
        Return: new amenity object
    """
    try:
        body_request = request.get_json(silent=True)
        if (body_request is None):
            abort(400, 'Not a JSON')
        amenity_name = body_request['name']
    except KeyError:
        abort(400, 'Missing name')
    new_amenity = amenity.Amenity(name=amenity_name)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict())


def do_update_amenity(amenity_id, request):
    """
        Updates a Amenity object
    """
    get_amenity = do_check_id(amenity_id)
    body_request = request.get_json(silent=True)
    if (body_request is None):
        abort(404, 'Not a JSON')
    for k, v in body_request.items():
        if (k not in ('id', 'created_at', 'updated_at')):
            setattr(get_amenity, k, v)
    storage.save()
    return jsonify(get_amenity.to_dict())


@app_views.route('/amenities/', methods=['GET', 'POST'],
                 defaults={'amenity_id': None})
@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenities(amenity_id):
    """
        Handle amenities requests with needed functions
    """
    if (request.method == "GET"):
        return do_get_amenities(amenity_id)
    elif (request.method == "DELETE"):
        return do_delete_amenity(amenity_id)
    elif (request.method == "POST"):
        return do_create_amenity(request), 201
    elif (request.method == "PUT"):
        return do_update_amenity(amenity_id, request), 200
