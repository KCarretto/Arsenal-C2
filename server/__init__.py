"""
This package represents an Arsenal HTTP C2 Server.
"""
from flask import Flask

def create_app(**config_overrides):
    """
    Creates a flask application with the desired configuration settings
    and connects it to the database.
    """
    app = Flask(__name__)
    from server.endpoint import ROUTES
    app.register_blueprint(ROUTES)
    app.config.update(config_overrides)

    return app
