from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models import state


@app_views.route('/states/', defaults={'state_id': None})
@app_views.route('/states/<state_id>')
def states(state_id):
    """
    Retrieves the list of all State objects
    if state_id is not none get a State object
    """
    if (state_id is not None):
        try:
            get_state = storage.get(state.State, state_id)
            get_state = get_state.to_dict()
        except Exception:
            abort(404)
        return jsonify(get_state)
    all_states = storage.all(state.State)
    states = []
    for v in all_states.values():
        states.append(v.to_dict())
    return jsonify(states)