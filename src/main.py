from lib import Request, serve 
from lib.logger import log
from typing import Tuple
import threading
import socket
import ssl
import os 
import yaml

with open('./config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())

os.chdir(config['file-dir'])

def handle_client(client: socket.socket, addr: Tuple[str, int]) -> None:
    request = bytes()

    while (data := client.recv(1024)):
        request += data

        if len(data) < 1024: break

    (request:=Request.from_bytes(request)) \
        .match() \
        .execute(request, client, addr) \
        .send(client)

    log.debug('destroy thread')

def main() -> None:
    http_thread = threading.Thread(name='http', target=serve, args=('0.0.0.0', config['http-port'], handle_client))
    https_thread = threading.Thread(name='https', target=serve, args=('0.0.0.0', config['https-port'], handle_client), kwargs=dict(wrapper=lambda socket: [
                ctx:=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER),
                ctx.load_cert_chain(certfile=config['ssl-cert'], keyfile=config['ssl-key']),
                ctx.wrap_socket(socket, server_side=True)
            ][-1]
        ))

    http_thread.start() if config['http-port'] else None
    https_thread.start() if config['https-port'] else None

if __name__ == '__main__': 
    main()

