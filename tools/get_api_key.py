"""
Generate an API Key for the C2.
"""
import os
import sys

from pyarsenal import APIException
from pyarsenal.tools.cli import build_cli, CLI


def main():
    try:
        cli: CLI = build_cli()
        key = cli.client.create_api_key(
            allowed_api_calls=["CreateSession", "SessionCheckIn", "GetCurrentContext"]
        )
        key_path = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "docker/arsenal_key")
        )
        with open(key_path, "w+") as f:
            f.write(key)
        os.chmod(key_path, 0o640)
        print(
            f"Successfully wrote API Key with restricted privileges to {key_path} \
            \nRun `docker-compose up -d --build` after configuring the c2. "
        )
    except IOError as e:
        print(f"Error trying to save key to file: {e}")
        sys.exit(1)
    except APIException as e:
        print(f"Error creating API key: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unhandled exception occurred while creating an API key: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
