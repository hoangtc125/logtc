import logging
import threading
import contextvars
from logging.handlers import TimedRotatingFileHandler

from .singleton import singleton
from .handler import SocketIOHandler
from .utils import setup_logging

request_id_context = contextvars.ContextVar('request_id_context', default="logtc")


class CustomFormatter(logging.Formatter):
    def format(self, record):
        record.request_id = request_id_context.get()
        return super().format(record)


@singleton
class Logger:
    def __init__(self):
        self.logger = logging.getLogger("logtc")
        self.handshake_path = None
        self.url = None
        self.formatter = None
        self.socket_handler = None

    def setup(self, name: str, log_path: str, when: str, interval: int, url: str, handshake_path: str):
        self.url = url
        self.handshake_path = handshake_path

        setup_logging(log_path)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = CustomFormatter('[%(levelname)s] - %(asctime)s - %(name)s - %(request_id)s - %(message)s')

        # Tạo handler cho file log xoay vòng
        file_handler = TimedRotatingFileHandler(filename=log_path, when=when, interval=interval)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)

    def __setup_socket_connection(self):
        self.socket_handler = SocketIOHandler(url=self.url, handshake_path=self.handshake_path)
        self.socket_handler.setLevel(logging.DEBUG)
        self.socket_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.socket_handler)
        print("add socket logging handler")

    def add_socket_logging(self):
        connect_thread = threading.Thread(target=self.__setup_socket_connection, args=())
        connect_thread.daemon = True
        connect_thread.start()

    def remove_socket_logging(self):
        if self.socket_handler:
            print("remove socket logging handler")
            self.logger.removeHandler(self.socket_handler)
