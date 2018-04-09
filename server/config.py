"""
This module contains configuration information for the server.
"""
API_KEY_FILE = '/opt/arsenal-c2/.arsenal_key'
TEAMSERVER_URI = 'http://qa.redteam-arsenal.com'

SERVER_ADDRESS = None   # Set this to override the public lookup of the server IP.
                        #This is used to determine the initial URI that session is beaconing to.

LOG_LEVEL = 'DEBUG'     # Set this to the desired log level of the server.
                        # Log levels: DEBUG, INFO, WARN, CRIT, FATAL
