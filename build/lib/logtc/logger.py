import logging
import threading
import contextvars
from logging.handlers import TimedRotatingFileHandler

from .singleton import singleton
from .handler import SocketIOHandler
from .utils import setup_logging

logtc_context = contextvars.ContextVar('logtc_context', default="logngo")


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.request_id = logtc_context.get()
        return super().format(record)


@singleton
class Logtc:
    def __init__(self):
        self.logger = logging.getLogger("logngo")
        self.logger.setLevel(logging.DEBUG)
        self.formatter = CustomFormatter(
            '%(request_id)s - [%(levelname)s] - %(asctime)s - %(name)s - %(filename)s - %(message)s'
        )
        self.file_handler = None
        self.socket_handler = None
        self.stream_handler = None

    def setup(self, name: str, formatter: str = None, level: int = logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.level = level
        if formatter:
            self.formatter = CustomFormatter(f"%(request_id)s - {formatter}")

    def setup_file_handler(self, file_path: str, when: str, interval: int):
        if self.file_handler:
            raise Exception("logngo: File handler existed")
        setup_logging(file_path)
        self.file_handler = TimedRotatingFileHandler(filename=file_path, when=when, interval=interval)
        self.file_handler.setLevel(self.level)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        print("logngo: Add file handler")

    def setup_socket_handler(self, url: str, handshake_path: str):
        self.__socket_url = url
        self.__socket_handshake_path = handshake_path

    def setup_stream_handler(self):
        if self.stream_handler:
            raise Exception("logngo: Stream handler existed")
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(self.level)
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)
        print("logngo: Add stream handler")

    def __setup_socket_connection(self):
        self.socket_handler = SocketIOHandler(
            url=self.__socket_url, handshake_path=self.__socket_handshake_path
        )
        self.socket_handler.setLevel(self.level)
        self.socket_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.socket_handler)
        print("logngo: Add socket handler")

    def add_socket_logging(self):
        connect_thread = threading.Thread(target=self.__setup_socket_connection, args=())
        connect_thread.daemon = True
        connect_thread.start()

    def remove_socket_logging(self):
        if self.socket_handler:
            print("logngo: Remove socket handler")
            self.logger.removeHandler(self.socket_handler)
