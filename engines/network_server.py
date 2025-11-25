"""
Network server engine - for the player hosting the game (plays as Black).
"""

from engines.network import NetworkServerEngine

class NetworkServer:
    """ Factory class that creates server engine with host/port. """
    def __new__(cls, host='0.0.0.0', port=12345):
        return NetworkServerEngine(host=host, port=port)

engine = NetworkServer

