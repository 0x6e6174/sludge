import socket
import threading
from typing import Callable

def serve(address: str, port: int, callback: Callable, wrapper: Callable[[socket.socket], socket.socket] = lambda s: s) -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            server_socket.bind((address, port))
            server_socket.listen(1)
            server_socket = wrapper(server_socket)

            while True:
                conn, addr = server_socket.accept()
                client_connection = threading.Thread(target=callback, args=(conn, addr))
                client_connection.start()

        except Exception as e:
            print(e)
    
        finally: server_socket.close()
