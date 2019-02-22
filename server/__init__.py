"""
This package represents an Arsenal HTTP C2 Server.
"""
import os
import sys

from flask import Flask
from pyarsenal import ArsenalClient


def create_app(**config_overrides):
    """
    Creates a flask application with the desired configuration settings
    and connects it to the database.
    """
    app = Flask(__name__)

    # Optionally configure server address
    app.config["SERVER_ADDRESS"] = os.environ.get("SERVER_ADDRESS")

    # Build config
    app.config.update(config_overrides)

    # Add pyarsenal client
    teamserver_uri = app.config.get(
        "TEAMSERVER_URI", os.environ.get("TEAMSERVER_URI", "http://redteam-arsenal.com/api")
    )
    api_key_file = app.config.get(
        "API_KEY_FILE", os.environ.get("API_KEY_FILE", "~/.arsenal/.api_key")
    )
    if not os.path.exists(api_key_file):
        print(f"ERROR: Cannot start C2 application without an API key ({api_key_file}).")
        sys.exit(1)
    app.arsenal_client = ArsenalClient(uri=teamserver_uri, api_key_file=api_key_file)

    from server.endpoint import ROUTES

    app.register_blueprint(ROUTES)

    return app
