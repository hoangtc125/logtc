import logging
import socketio
import traceback


class SocketIOHandler(logging.Handler):
    def __init__(self, url: str, handshake_path: str):
        super().__init__()
        self.sio = socketio.Client()
        self.url = url
        self.handshake_path = handshake_path
        self.channel = "__logtc"
        self._connect()

    def _connect(self):
        try:
            self.sio.connect(url=self.url, socketio_path=self.handshake_path)
        except Exception as e:
            traceback.print_exc()

    def emit(self, record):
        try:
            self.sio.emit(self.channel, self.format(record))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self.sio.disconnect()
        super().close()
