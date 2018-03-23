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
    # TODO: Update target facts
    mac_addrs = None
    try:
        interfaces = data['facts']['interfaces']
        mac_addrs = [interface['mac_addr'] for interface in interfaces]
    except KeyError:
        # Legacy Format Support
        interfaces = data['interfaces']
        mac_addrs = interfaces.keys()

    # TODO: Implement exception handling if proper data was not received

    # TODO: Implement Fact submission

    config = data.get('config', {})
    servers = config.get('servers', [SERVER_ADDRESS if SERVER_ADDRESS else public_ip()])
    interval = config.get('interval', -1)
    interval_delta = config.get('interval_delta', -1)

    session_id = Session.create_session(mac_addrs, servers, interval, interval_delta, config)
    resp = Session.session_checkin(session_id, data.get('responses'))

    return resp

def existing_agent(data):
    """
    This handler is called when an agent with a session id checks in.
    """
    # TODO: Implement exception handling
    session_id = data['session_id']
    config = data.get('config', {})
    if config:
        Session.update_session_config(
            session_id,
            interval=config.get('interval'),
            interval_delta=config.get('interval_delta'),
            servers=config.get('servers'),
            config_dict=config)

    # TODO: Handle session does not exist
    resp = Session.session_checkin(session_id, data.get('responses'))

    return resp

