from socket import socket
from typing import Dict
from .responsecodes import ResponseCode

class Response:
    def __init__(self, code: ResponseCode, headers: Dict[str, str], body: bytes):
        self.code = code
        self.headers = headers
        self.body = body

    def build_response(self) -> bytes: 
        return (
            f"HTTP/1.1 {str(self.code)}\r\n".encode('utf-8')
            + f"{''.join([f"{key}: {value}\r\n" for key, value in self.headers.items()])}\r\n".encode('utf-8')
            + self.body
        )

    def send(self, client: socket) -> None:
        print(self)
        client.sendall(self.build_response())
        client.close()
