"""
    This module contains all valid server endpoints.
"""
from flask import Blueprint, request, jsonify
from .handlers import new_agent, existing_agent
from .exceptions import InvalidRequest
from .utils import log, error_response
from .client import ArsenalClient
from .config import API_KEY_FILE, TEAMSERVER_URI
ROUTES = Blueprint('endpoint', __name__)

CLIENT = ArsenalClient(teamserver_uri=TEAMSERVER_URI, api_key_file=API_KEY_FILE)

@ROUTES.route('/', methods=['POST'])
def handle_agent():
    """
    This method handles any incoming agent connections.
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id')

        resp = {
            'error': True
        }

        if not session_id:
            session_id = new_agent(CLIENT, data)
            data['session_id'] = session_id

        log("Checking in {}".format(session_id))

        resp = existing_agent(CLIENT, data)

        json_resp = jsonify(resp)
        json_resp.headers['Connection'] = 'close'

        return json_resp
    except InvalidRequest as exception:
        json_resp = jsonify(
            error_response(400, exception.name, str(exception))
        )
        json_resp.headers['Connection'] = 'close'

        return json_resp

@ROUTES.route('/test', methods=['GET', 'POST'])
def test_response():
    """
    This function will return a sample of a standard response using static data.
    """
    resp = jsonify({
        "session_id": "Your Session ID",
        "actions": [
            {
                "action_id": "some action ID to track",
                "command": "echo",
                "args": ["hi dad"],
                "action_type": 0
            },
            {
                "action_id": "Configuration update action id",
                "action_type": 6,
                "config": {
                    "interval": 10,
                    "servers": ["10.10.10.10", "1.2.3.4"]
                }
            }
        ]
    })
    resp.headers['Connection'] = 'close'
    return resp
