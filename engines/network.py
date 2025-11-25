"""
Network engine for Othello game - allows two players to play over network using sockets.
One player acts as server (host), the other as client (connects to server).

Usage:
    Server (Black player): python othello.py network_server network_receiver <host> <port>
    Client (White player): python othello.py network_receiver network_client <host> <port>
"""

import socket
import threading
import json
from board import print_moves
from engines import Engine


# Global connection manager to share connection between engines on same side
_connection_manager = None


class ConnectionManager:
    """ Manages shared network connection between server/client engines. """
    
    def __init__(self):
        self.socket = None
        self.connection = None
        self.address = None
        self.lock = threading.Lock()
        self.connected = False
        self.opponent_move = None
        self.move_received = threading.Event()
        self.listen_thread = None
    
    def setup_server(self, host='0.0.0.0', port=12345):
        """ Set up as server. """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((host, port))
            self.socket.listen(1)
            print(f"\n[Server] Waiting for client connection on port {port}...")
            
            self.connection, self.address = self.socket.accept()
            self.connected = True
            print(f"[Server] Client connected from {self.address}")
            
            # Send handshake
            handshake = {"type": "handshake", "color": -1}
            self._send_data(handshake)
            
            self._start_listening()
            
        except Exception as e:
            print(f"[Server] Error: {e}")
            raise
    
    def setup_client(self, host='localhost', port=12345):
        """ Set up as client. """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"\n[Client] Connecting to server at {host}:{port}...")
            
            self.socket.connect((host, port))
            self.connection = self.socket
            self.connected = True
            print(f"[Client] Connected to server!")
            
            # Receive handshake
            handshake = self._receive_data()
            if handshake and handshake.get("type") == "handshake":
                print(f"[Client] Handshake received")
            
            self._start_listening()
            
        except Exception as e:
            print(f"[Client] Error: {e}")
            raise
    
    def _start_listening(self):
        """ Start background thread to listen for moves. """
        self.listen_thread = threading.Thread(target=self._listen_for_moves, daemon=True)
        self.listen_thread.start()
    
    def _listen_for_moves(self):
        """ Background thread to listen for opponent moves. """
        while self.connected:
            try:
                data = self._receive_data()
                if data:
                    if data.get("type") == "move":
                        with self.lock:
                            move = tuple(data["move"])
                            self.opponent_move = move
                            self.move_received.set()
                            x, y = move
                            move_str = chr(ord('a') + x) + str(y + 1)
                            print(f"\n[Network] Received opponent move: {move_str}")
                    elif data.get("type") == "game_over":
                        print(f"\n[Network] Game over: {data.get('message', '')}")
                        break
            except Exception as e:
                if self.connected:
                    print(f"Error in listen thread: {e}")
                break
    
    def _send_data(self, data):
        """ Send data over network. """
        try:
            if self.connection:
                message = json.dumps(data).encode('utf-8')
                length = len(message)
                self.connection.sendall(length.to_bytes(4, byteorder='big'))
                self.connection.sendall(message)
        except Exception as e:
            print(f"Error sending data: {e}")
            self.connected = False
    
    def _receive_data(self):
        """ Receive data from network. """
        try:
            if self.connection:
                length_bytes = self.connection.recv(4)
                if not length_bytes:
                    return None
                length = int.from_bytes(length_bytes, byteorder='big')
                
                data = b''
                while len(data) < length:
                    chunk = self.connection.recv(length - len(data))
                    if not chunk:
                        return None
                    data += chunk
                
                return json.loads(data.decode('utf-8'))
        except Exception as e:
            if self.connected:
                print(f"Error receiving data: {e}")
            self.connected = False
            return None
    
    def send_move(self, move):
        """ Send move to opponent. """
        move_data = {"type": "move", "move": list(move)}
        self._send_data(move_data)
    
    def wait_for_move(self, timeout=300):
        """ Wait for opponent's move. """
        self.move_received.clear()
        if self.move_received.wait(timeout=timeout):
            with self.lock:
                move = self.opponent_move
                self.opponent_move = None
                return move
        else:
            raise TimeoutError("Timeout waiting for opponent move")
    
    def close(self):
        """ Close connection. """
        self.connected = False
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
        if self.socket:
            try:
                self.socket.close()
            except:
                pass


class NetworkServerEngine(Engine):
    """ Network engine for server side (Black player). """
    
    def __init__(self, host='0.0.0.0', port=12345):
        global _connection_manager
        if _connection_manager is None:
            _connection_manager = ConnectionManager()
            _connection_manager.setup_server(host, port)
            print("[Server] You are playing as BLACK (-1)")
        self.conn = _connection_manager
        self.my_color = -1
    
    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Get move - if my turn, get input; else wait for network. """
        if color == self.my_color:
            return self._get_my_move(board, color)
        else:
            return self._get_opponent_move()
    
    def _get_my_move(self, board, color):
        """ Get move from local player. """
        legal_moves = board.get_legal_moves(color)
        print(f"\n[Your turn - BLACK] Enter your move: ", end='')
        user_input = input().strip()
        move = self.parse_input(legal_moves, user_input)
        
        while move is None:
            print("Invalid move. Legal moves:")
            print_moves(sorted(legal_moves))
            print(f"\n[Your turn - BLACK] Enter your move: ", end='')
            user_input = input().strip()
            move = self.parse_input(legal_moves, user_input)
        
        self.conn.send_move(move)
        x, y = move
        move_str = chr(ord('a') + x) + str(y + 1)
        print(f"[Network] Sent move: {move_str}")
        return move
    
    def _get_opponent_move(self):
        """ Wait for opponent's move. """
        print("\n[Waiting] Waiting for opponent's move...")
        return self.conn.wait_for_move()
    
    @staticmethod
    def parse_input(legal_moves, user_input):
        """ Parse and validate move input. """
        if len(user_input) == 2:
            xc = user_input[0].lower()
            yc = user_input[1].lower()
            if 'a' <= xc <= 'h' and '1' <= yc <= '8':
                x = ord(xc) - ord('a')
                y = int(yc) - 1
                move = (x, y)
                if move in legal_moves:
                    return move
        return None


class NetworkClientEngine(Engine):
    """ Network engine for client side (White player). """
    
    def __init__(self, host='localhost', port=12345):
        global _connection_manager
        if _connection_manager is None:
            _connection_manager = ConnectionManager()
            _connection_manager.setup_client(host, port)
            print("[Client] You are playing as WHITE (1)")
        self.conn = _connection_manager
        self.my_color = 1
    
    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Get move - if my turn, get input; else wait for network. """
        if color == self.my_color:
            return self._get_my_move(board, color)
        else:
            return self._get_opponent_move()
    
    def _get_my_move(self, board, color):
        """ Get move from local player. """
        legal_moves = board.get_legal_moves(color)
        print(f"\n[Your turn - WHITE] Enter your move: ", end='')
        user_input = input().strip()
        move = self.parse_input(legal_moves, user_input)
        
        while move is None:
            print("Invalid move. Legal moves:")
            print_moves(sorted(legal_moves))
            print(f"\n[Your turn - WHITE] Enter your move: ", end='')
            user_input = input().strip()
            move = self.parse_input(legal_moves, user_input)
        
        self.conn.send_move(move)
        x, y = move
        move_str = chr(ord('a') + x) + str(y + 1)
        print(f"[Network] Sent move: {move_str}")
        return move
    
    def _get_opponent_move(self):
        """ Wait for opponent's move. """
        print("\n[Waiting] Waiting for opponent's move...")
        return self.conn.wait_for_move()
    
    @staticmethod
    def parse_input(legal_moves, user_input):
        """ Parse and validate move input. """
        if len(user_input) == 2:
            xc = user_input[0].lower()
            yc = user_input[1].lower()
            if 'a' <= xc <= 'h' and '1' <= yc <= '8':
                x = ord(xc) - ord('a')
                y = int(yc) - 1
                move = (x, y)
                if move in legal_moves:
                    return move
        return None


class NetworkReceiverEngine(Engine):
    """ Engine that only receives moves from network (for opponent's color). """
    
    def __init__(self):
        global _connection_manager
        if _connection_manager is None:
            raise RuntimeError("Connection manager not initialized. Use network_server or network_client first.")
        self.conn = _connection_manager
    
    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        """ Always wait for network move (this is always opponent's turn). """
        player_name = {-1: "BLACK", 1: "WHITE"}
        print(f"\n[Waiting] Waiting for opponent's move ({player_name[color]})...")
        return self.conn.wait_for_move()


# Default export (for backward compatibility, but should use network_server or network_client)
engine = NetworkServerEngine

