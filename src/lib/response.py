from socket import socket
from typing import Dict
from .responsecodes import ResponseCode
from .logger import log 

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
        log.debug(f'sending {self} to {client}') 
        client.sendall(self.build_response())
        client.close()

    def __repr__(self): 
        return f'Response(code={self.code}, headers={self.headers}, body={self.body[:256]})'
