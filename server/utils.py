"""
This module contains helper functions to be utilized by the C2.
"""
import requests

#from .config import LOG_LEVEL

def error_response(status, error_type, description):
    """
    Formats an error response.
    """
    return {
        'status': status,
        'error_type': error_type,
        'description': description,
        'error': True,
    }

def log(msg, level='DEBUG'):
    """
    Log a message.
    """
    print('[{}]{}'.format(level, msg))

def public_ip():
    """
    This method returns the public facing ip address of the server.
    """
    return requests.get("http://ipecho.net/plain?").text
