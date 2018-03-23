"""
    This runs the c2 using a Flask webserver (not recommended for production use).
"""

from server import create_app

SERVER = create_app()

if __name__ == '__main__':
    SERVER.run(debug=False, host='0.0.0.0', port=8080)
