from flask_socketio import SocketIO
import logging

class SocketService:
    socketio = None
    logger = logging.getLogger(__name__)

    @classmethod
    def init_app(cls, app):
        cls.socketio = SocketIO(
            app,
            cors_allowed_origins=["http://localhost:3000", "http://frontend:3000"],
            async_mode='eventlet',
            logger=True,
            engineio_logger=True
        )
        cls._register_handlers()
        return cls.socketio

    @classmethod
    def _register_handlers(cls):
        @cls.socketio.on('connect')
        def handle_connect():
            cls.logger.info("Client connected")
            return True

        @cls.socketio.on('client_ready')
        def handle_client_ready():
            cls.logger.info("Client ready to receive data")

        @cls.socketio.on('disconnect')
        def handle_disconnect():
            cls.logger.info("Client disconnected")

        @cls.socketio.on_error()
        def error_handler(e):
            cls.logger.error(f"SocketIO error: {str(e)}")

    def emit(self, event, data):
        try:
            if self.socketio:
                self.socketio.emit(event, data)
                self.logger.debug(f"Emitted {event} event with data: {data}")
        except Exception as e:
            self.logger.error(f"Error emitting {event}: {str(e)}")

socket_service = SocketService() 