"""
This module contains helper functions to be utilized by the C2.
"""
import requests

def public_ip():
    """
    This method returns the public facing ip address of the server.
    """
    return requests.get("http://ipecho.net/plain?").text
