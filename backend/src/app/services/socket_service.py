from flask_socketio import SocketIO

class SocketService:
    def __init__(self, server_url):
        self.socketio = SocketIO(message_queue=server_url, logger=True, engineio_logger=True)
        self.socketio.connect(server_url)
        print(f"Connected to Socket.IO server at {server_url}")
        
    def emit_data(self, event, data):
        try:
            print(f"Emitting data: {data}")
            self.socketio.emit(event, data)
        except Exception as e:
            print(f"Error emitting data: {e}")
    
    def close_connection(self):
        self.socketio.disconnect()
        print("Socket connection closed")