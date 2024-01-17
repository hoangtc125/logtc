import socketio

from .singleton import singleton
from .main import Logger


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
        self.__socket_logging_client = set()

        @self.__sio.on("connect")
        async def handle_connect(sid, environ):
            source = get_source(environ)
            if source == "subscriber":
                if len(self.__socket_logging_client) == 0:
                    Logger().add_socket_logging()
                self.__socket_logging_client.add(sid)
                print(f"logngo: Subscriber connected {self.__socket_logging_client}")
            else:
                print(f"logngo: Publisher connected")

        @self.__sio.on("disconnect")
        async def handle_disconnect(sid):
            if sid in self.__socket_logging_client:
                self.__socket_logging_client.discard(sid)
                print(f"logngo: Subscriber disconnected {self.__socket_logging_client}")
                if len(self.__socket_logging_client) == 0:
                    Logger().remove_socket_logging()
            else:
                print("logngo: Publisher disconnected")

        @self.__sio.on("__logngo")
        async def handle_message(sid, data):
            await self.__sio.emit("logngo", data)

    def __call__(self):
        return self.__asgi


socket_ngo = Socket()
