"""
This module contains exceptions raised by the C2.
"""

class InvalidRequest(Exception):
    """
    This exception is raised if a malformed request was sent to the C2.
    """
    name = 'invalid-request'
