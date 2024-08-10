from typing import Dict, Any
import json
from urllib.parse import parse_qs
from requests_toolbelt.multipart import decoder

class Body:
    def __init__(self, content: bytes, content_type: str):
        self.content = content
        self.content_type = content_type
        self.data = self.parse_body()

    def parse_body(self) -> Dict[str, Any]:
        if 'application/x-www-form-urlencoded' in self.content_type:
            return self.parse_form_urlencoded()
        elif 'application/json' in self.content_type:
            return self.parse_json()
        elif 'multipart/form-data' in self.content_type:
            boundary = self.content_type.split('boundary=')[1]
            return self.parse_multipart(boundary)
        else:
            return {}

    def parse_form_urlencoded(self) -> Dict[str, Any]:
        return {key: value[0] if len(value) == 1 else value for key, value in parse_qs(self.content.decode('utf-8')).items()}

    def parse_json(self) -> Dict[str, Any]:
        return json.loads(self.content.decode('utf-8'))

    def parse_multipart(self, boundary: str) -> Dict[str, Any]:
        multipart_data = decoder.MultipartDecoder(self.content, boundary)
        fields = {}
        for part in multipart_data.parts:
            fields[part.headers['Content-Disposition'].split('=')[1].strip('"')] = part.text
        return fields

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return f'Body({self.content=}, {self.content_type=}, {self.data=})'
