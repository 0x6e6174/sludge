from urllib.parse import urlsplit, unquote, parse_qs

class Path:
    def __init__(self, route: str):
        self.route = route
        self.reduce_url()
        self.get_params()

    def reduce_url(self):
        _, _, path, _, _ = urlsplit(self.route)

        path = unquote(path)

        segments = []
        for segment in path.split('/'):
            if segment != '..':
                segments.append(segment)
            elif segments and segments[-1] != '..':
                segments.pop()

        reduced_path = '/'.join(segments)

        self.path = reduced_path

    def get_params(self): 
        _, _, _, query, _ = urlsplit(self.route)
        self.params = {key: value[0] if len(value) == 1 else value for key, value in parse_qs(query).items()}

    def __repr__(self):
        return f"Path({self.route=}, {self.path=}, {self.params=})"

