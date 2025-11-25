"""
Network client engine - for the player connecting to server (plays as White).
"""

from engines.network import NetworkClientEngine

class NetworkClient:
    """ Factory class that creates client engine with host/port. """
    def __new__(cls, host='localhost', port=12345):
        return NetworkClientEngine(host=host, port=port)

engine = NetworkClient

