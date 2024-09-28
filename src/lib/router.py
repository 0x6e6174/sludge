from dataclasses import dataclass
from socket import socket
from datetime import datetime
from functools import reduce
from typing import List, Callable, Tuple 
from .method import Method
from .response import Response
from .responsecodes import ResponseCode
from .content import *
from .patchers import patchers
from .logger import log
import os
import traceback
import mimetypes
import hashlib

@dataclass
class Route: 
    matcher: Callable 
    methods: List[Method]
    handler: Callable[['Request', socket, Tuple[str, int]], Response]

    def method_is_allowed(self, method: Method) -> bool: 
        return method in self.methods 

    def execute(self, *args): 
        try: 
            response = self.handler(*args)
            for patcher in patchers:
                response = patcher(response, args[0])

            return response

        except Exception as e:
            log.error(traceback.format_exc)
            return error_page(500)

    def matches(self, request: 'Request') -> bool:
        if not self.method_is_allowed(request.method): return False
        return self.matcher(request.path)

def generate_opengraph_html(file_url):
    print('FILE URL: ', file_url)
    mime_type, _ = mimetypes.guess_type(file_url)

    file_name = os.path.basename(file_url)

    if mime_type and mime_type.startswith('image/'):
        content_type = 'image'
        embed_html = f'<img src="{file_url}" alt="{file_name}" style="max-width: 100%; height: auto;">'
    elif mime_type and mime_type.startswith('video/'):
        content_type = 'video'
        embed_html = f'<video controls style="max-width: 100%;"><source src="{file_url}" type="{mime_type}">your browser does not support the video tag.</video>'
    else:
        content_type = 'document'
        embed_html = f'<iframe src="{file_url}" title="{file_name}" style="width: 100%; height: 600px; border: none;"></iframe>'

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Embed File: {file_name}</title>
    
    <!-- OpenGraph Meta Tags -->
    <meta property="og:title" content="{file_name}" />
    <meta property="og:type" content="{content_type}" />
    <meta property="og:url" content="{file_url}" />
    <meta property="og:description" content="Embedded file: {file_name}" />
    <meta property="og:image" content="URL_TO_AN_IMAGE" /> <!-- Optional: Replace with an actual image URL -->
    
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
        }}
    </style>
</head>
<body>
    <p>{file_name}</p>
    <hr>
    {embed_html}
</body>
</html>
"""
    return html_content

def is_subdict(sub_dict, main_dict):
    for key, value in sub_dict.items():
        if key not in main_dict or main_dict[key] != value:
            return False
    return True

def compute_md5(file_path):
    md5_hash = hashlib.md5()
    
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    
    return md5_hash.hexdigest()

routes = [
    Route(
        lambda request: request.path == '/',
        [Method.GET],
        lambda *_: Response(
            ResponseCode.OK,
            {'Content-Type': 'text/html'},
            parse_file('index.html').encode('utf-8')
        )
    ),
    Route(
        lambda request: [print(os.getcwd(), '.'+request.path, request.params, os.path.isfile('.'+request.path)), os.path.isfile('.'+request.path) and is_subdict({'embed': 'true'}, request.params)][-1], 
        [Method.GET], 
        lambda request, *_: Response(
            ResponseCode.OK,
            {'Content-Type': 'text/html'},
            generate_opengraph_html(f'https://natalieee.net{request.path.path}?hash={request.path.params['hash']}').encode('utf-8')
        ) 
    ),
    Route(
        lambda request: [print(os.getcwd(), '.'+request.path, request.params, os.path.isfile('.'+request.path)), os.path.isfile('.'+request.path)][-1], 
        [Method.GET], 
        lambda request, *_: Response(
            ResponseCode.OK, 
            *raw_file_contents('.'+request.path.path)
        ) if request.path.params['hash'] == compute_md5('.'+request.path.path) else error_page(403)
    )
]

