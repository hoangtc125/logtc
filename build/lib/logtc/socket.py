import socketio

from .singleton import singleton
from .logger import Logtc


def get_source(environ):
    query_params = environ.get("QUERY_STRING", "")
    query_dict = dict(qc.split("=") for qc in query_params.split("&"))
    client_id = query_dict.get("source")
    return client_id


@singleton
class Socket:
    def __init__(self):
        self.__sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
        self.__asgi = socketio.ASGIApp(self.__sio)
        self.__socket_logging_client = None

        @self.__sio.on("connect")
        async def handle_connect(sid, environ):
            source = get_source(environ)
            if source == "subscriber":
                self.__socket_logging_client = sid
                Logtc().add_socket_logging()
                print(f"logngo: Subscriber connected {self.__socket_logging_client}")
            else:
                print(f"logngo: Publisher connected")

        @self.__sio.on("disconnect")
        async def handle_disconnect(sid):
            if sid == self.__socket_logging_client:
                Logtc().remove_socket_logging()
                print(f"logngo: Subscriber disconnected {sid}")
            else:
                print("logngo: Publisher disconnected")

        @self.__sio.on("__logtc")
        async def handle_message(sid, data):
            await self.__sio.emit("logngo", data)

    def __call__(self):
        return self.__asgi


sockettc = Socket()
