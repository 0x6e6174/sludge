from dataclasses import dataclass 

from .method import Method 
from .path import Path 
from .headers import Headers 
from .body import Body
from .router import routes
from .logger import log

@dataclass
class Request:
    method: Method 
    path: Path
    version: float 
    headers: Headers
    body: Body

    @classmethod
    def from_bytes(cls, request_bytes: bytes):
        request_str = request_bytes.decode('utf-8')
        lines = request_str.split('\r\n')
        
        request_line = lines[0].split()
        
        if len(request_line) != 3:
            raise ValueError("Invalid request line")

        method, path, version_str = request_line
        version = float(version_str.split('/')[1])

        method = Method(method)
        path = Path(path)

        headers = Headers({})
        body = b''

        header_lines = lines[1:]
        for header_line in header_lines:
            if header_line == '':
                break
            key, value = header_line.split(':', 1)
            headers.add(key.strip(), value.strip())

        body_start = request_str.find('\r\n\r\n') + 4
        body = Body(request_bytes[body_start:], headers.get('Content-Type') or 'text/plain')

        if not 'Nim httpclient' in headers.get('user-agent'):
            log.info(f'received request for {path.path} from {headers.get('X-Real-IP')}')

        return cls(method, path, version, headers, body)

    def match(self):
        for route in routes: 
            if route.matches(self):
                log.debug(f'matched {self} with {route}')
                return route

    def __repr__(self):
        path_repr = repr(self.path)
        body_repr = repr(self.body)
        return (f"Request(method={self.method!r}, path={path_repr}, version={self.version!r}, "
                f"headers={self.headers!r}, body={body_repr})")

