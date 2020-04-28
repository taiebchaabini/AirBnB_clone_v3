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
        get_state = get_state
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

@app_views.route('/states/', defaults={'state_id': None})
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def states(state_id):
    """
        Handle states requests with needed functions
    """
    if (request.method == "GET"):
        return do_get_states(state_id)
    elif (request.method == "DELETE"):
        return do_delete_state(state_id)