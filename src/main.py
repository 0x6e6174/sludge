from lib import Request, serve 
from typing import Tuple
import threading
import socket
import ssl
import os 

os.chdir('site')

def handle_client(client: socket.socket, addr: Tuple[str, int]) -> None:
    request = bytes()

    while (data := client.recv(1024)):
        request += data
        print(len(data), data)

        if len(data) < 1024: break

    (request:=Request.from_bytes(request)) \
        .match() \
        .execute(request, client, addr) \
        .send(client)

def main() -> None:
    http_thread = threading.Thread(name='http', target=serve, args=('0.0.0.0', 5000, handle_client))
    https_thread = threading.Thread(name='https', target=serve, args=('0.0.0.0', 6001, handle_client), kwargs=dict(wrapper=lambda socket: [
                ctx:=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER),
                ctx.load_cert_chain(certfile='./badcert.pem', keyfile='./badkey.pem'),
                ctx.wrap_socket(socket, server_side=True)
            ][-1]
        ))

    http_thread.start()
    #https_thread.start()

if __name__ == '__main__': 
    main()

