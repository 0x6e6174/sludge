import socket
import threading
import traceback
from typing import Callable

from .logger import log

def serve(address: str, port: int, callback: Callable, wrapper: Callable[[socket.socket], socket.socket] = lambda s: s) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log.info(f'server started on {port}')
    try: 
        server_socket.bind((address, port))
        server_socket.listen(1)
        server_socket = wrapper(server_socket)

        while True:
            try:
                conn, addr = server_socket.accept()
                client_connection = threading.Thread(target=callback, args=(conn, addr))
                client_connection.start()

            except Exception:
                log.warn(traceback.format_exc())

    except: 
        log.critical(traceback.format_exc())

    finally: 
        server_socket.close()
        log.info(f'server on {port} shut down')
