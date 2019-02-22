"""
    This module contains all valid server endpoints.
"""
from flask import Blueprint, request, jsonify, current_app

from .handlers import new_agent, existing_agent
from .exceptions import InvalidRequest
from .utils import log, error_response

ROUTES = Blueprint("endpoint", __name__)


@ROUTES.route("/", methods=["POST"])
def handle_agent():
    """
    This method handles any incoming agent connections.
    """
    try:
        data = request.get_json()
        session_id = data.get("session_id")

        resp = {"error": True}

        if not session_id:
            session_id = new_agent(current_app.arsenal_client, data)
            data["session_id"] = session_id

        log("Checking in {}".format(session_id))

        resp = existing_agent(current_app.arsenal_client, data)

        json_resp = jsonify(resp)
        json_resp.headers["Connection"] = "close"

        return json_resp

    # Handle exception where agent provides invalid request
    except InvalidRequest as exception:
        json_resp = jsonify(error_response(400, exception.name, str(exception)))
        json_resp.headers["Connection"] = "close"

        return json_resp

    # Catch unhandled exceptions, and attempt to log an error to the teamserver
    except Exception as exception:  # pylint: disable=broad-except
        json_resp = jsonify(error_response(400, "unhandled-exception", str(exception)))
        json_resp.headers["Connection"] = "close"

        try:
            current_app.arsenal_client.create_log(
                "arsenal-c2",
                "CRIT",
                "[{}] {}".format(
                    current_app.config.get("SERVER_ADDRESS", "UNKNOWN_SERVER"), str(exception)
                ),
            )
        except Exception as e:  # pylint: disable=broad-except
            print(f"CRITICAL ERROR HANDLING UNHANDLED EXCEPTION: {e}")

        return json_resp


@ROUTES.route("/status", methods=["GET", "POST"])
def get_status():
    """
    Return status information about the C2.
    """
    connected = False
    try:
        current_app.arsenal_client.get_current_context()
        connected = True
    except Exception:  # pylint: disable=broad-except
        pass

    has_api_key = True if current_app.arsenal_client.api_key else False

    json_resp = jsonify(
        {
            "status": 200,
            "state": "running",
            "teamserver_connected": connected,
            "api_key": has_api_key,
        }
    )

    if not connected or not has_api_key:
        json_resp.status_code = 500

    return json_resp


@ROUTES.route("/test", methods=["GET", "POST"])
def test_response():
    """
    This function will return a sample of a standard response using static data.
    """
    resp = jsonify(
        {
            "session_id": "Your Session ID",
            "actions": [
                {
                    "action_id": "some action ID to track",
                    "command": "echo",
                    "args": ["hi dad"],
                    "action_type": 0,
                },
                {
                    "action_id": "Configuration update action id",
                    "action_type": 6,
                    "config": {"interval": 10, "servers": ["10.10.10.10", "1.2.3.4"]},
                },
            ],
        }
    )
    resp.headers["Connection"] = "close"
    return resp
