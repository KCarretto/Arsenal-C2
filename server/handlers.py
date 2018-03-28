"""
This module contains handlers that will deal with incoming connections.
"""
from .client import Session
from .config import SERVER_ADDRESS
from .utils import public_ip

def new_agent(data):
    """
    This handler is called when an agent checks in and does not have an existing session id.
    """
    mac_addrs = None

    facts = data.get('facts')
    if facts and isinstance(facts, dict):
        mac_addrs = [interface['mac_addr'] for interface in data['facts']['interfaces']]
    else:
        # Legacy Format Support
        mac_addrs = data['interfaces'].keys()

    # TODO: Implement exception handling if proper data was not received

    config = data.get('config', {})
    servers = config.get('servers', [SERVER_ADDRESS if SERVER_ADDRESS else public_ip()])
    interval = config.get('interval', -1)
    interval_delta = config.get('interval_delta', -1)

    return Session.create_session(mac_addrs, servers, interval, interval_delta, config, facts)

def existing_agent(data):
    """
    This handler is called when an agent with a session id checks in.
    """
    # TODO: Implement exception handling
    session_id = data['session_id']

    # TODO: Handle session does not exist
    resp = Session.session_checkin(
        session_id,
        data.get('responses'),
        data.get('config'),
        data.get('facts'))

    resp['actions'] = [action.raw_json for action in resp['actions']]

    return resp
