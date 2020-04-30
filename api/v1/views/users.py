#!/usr/bin/python3
""" Users routes handler """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import user


def do_check_id(cls, user_id):
    """
        If the user_id is not linked to any User object, raise a 404 error
    """
    try:
        get_user = storage.get(cls, user_id)
        get_user.to_dict()
    except Exception:
        abort(404)
    return get_user


def do_get_users(user_id):
    """
       Retrieves the list of all User objects
       if user_id is not none get a User object
    """
    if (user_id is not None):
        get_user = do_check_id(user.User, user_id).to_dict()
        return jsonify(get_user)
    all_users = storage.all(user.User)
    users = []
    for v in all_users.values():
        users.append(v.to_dict())
    return jsonify(users)


def do_delete_user(user_id):
    """
        Deletes a User object
        Return: an empty dictionary with the status code 200
    """
    get_user = do_check_id(user.User, user_id)
    storage.delete(get_user)
    storage.save()
    response = {}
    return jsonify(response)


def do_create_user(request):
    """
        Creates a user object
        Return: new user object
    """
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    try:
        email = body_request['email']
        password = body_request['password']
    except KeyError as e:
        errorMsg = 'Missing email'
        if (str(e) == "'password'"):
            errorMsg = 'Missing password'
        abort(400, errorMsg)
    new_user = user.User(email=email, password=password)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict())


def do_update_user(user_id, request):
    """
        Updates a User object
    """
    get_user = do_check_id(user.User, user_id)
    body_request = request.get_json()
    if (body_request is None):
        abort(400, 'Not a JSON')
    for k, v in body_request.items():
        if (k not in ('id', 'created_at', 'updated_at')):
            setattr(get_user, k, v)
    storage.save()
    return jsonify(get_user.to_dict())


@app_views.route('/users/', methods=['GET', 'POST'],
                 defaults={'user_id': None}, strict_slashes=False)
@app_views.route('/users/<user_id>',
                 methods=['GET', 'DELETE', 'PUT'])
def users(user_id):
    """
        Handle users requests with needed functions
    """
    if (request.method == "GET"):
        return do_get_users(user_id)
    elif (request.method == "DELETE"):
        return do_delete_user(user_id)
    elif (request.method == "POST"):
        return do_create_user(request), 201
    elif (request.method == "PUT"):
        return do_update_user(user_id, request), 200
