#!/usr/bin/python3
""" States routes handler """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import state


def do_check_id(state_id):
    """
        If the state_id is not linked to any State object, raise a 404 error
    """
    try:
        get_state = storage.get(state.State, state_id)
        get_state.to_dict()
    except Exception:
        abort(404)
    return get_state


def do_get_states(state_id):
    """
       Retrieves the list of all State objects
       if state_id is not none get a State object
    """
    if (state_id is not None):
        get_state = do_check_id(state_id).to_dict()
        return jsonify(get_state)
    all_states = storage.all(state.State)
    states = []
    for v in all_states.values():
        states.append(v.to_dict())
    return jsonify(states)


def do_delete_state(state_id):
    """
        Deletes a State object
        Return: an empty dictionary with the status code 200
    """
    get_state = do_check_id(state_id)
    storage.delete(get_state)
    storage.save()
    response = {}
    return jsonify(response)


def do_create_state(request):
    """
        Creates a state object
        Return: new state object
    """
    try:
        body_request = request.get_json(silent=True)
        if (body_request is None):
            abort(400, 'Not a JSON TEST')
        state_name = body_request['name']
    except KeyError:
        abort(400, 'Missing name')
    new_state = state.State(name=state_name)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict())


def do_update_state(state_id, request):
    """
        Updates a State object
    """
    get_state = do_check_id(state_id)
    body_request = request.get_json(silent=True)
    if (body_request is None):
        abort(404, 'Not a JSON')
    for k, v in body_request.items():
        if (k not in ('id', 'created_at', 'updated_at')):
            setattr(get_state, k, v)
    storage.save()
    return jsonify(get_state.to_dict())


@app_views.route('/states/', methods=['GET', 'POST'],
                 defaults={'state_id': None})
@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'])
def states(state_id):
    """
        Handle states requests with needed functions
    """
    if (request.method == "GET"):
        return do_get_states(state_id)
    elif (request.method == "DELETE"):
        return do_delete_state(state_id)
    elif (request.method == "POST"):
        return do_create_state(request), 201
    elif (request.method == "PUT"):
        return do_update_state(state_id, request), 200
