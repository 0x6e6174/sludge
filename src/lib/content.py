from typing import Dict, Tuple
import bleach 
import mimetypes
import subprocess
import re
import os
from .response import Response 
from .responsecodes import ResponseCode

env = os.environ.copy()
env["PATH"] = "./scripts/:" + env["PATH"]

def execute_bash_code(match: re.Match) -> str:
    code = match.group(1)
    result = subprocess.check_output(code, shell=True, executable='bash', env=env)
    return result.decode().strip()

def parse(string: str) -> str:
    return re.sub(r'\$\[(.*?)\]', execute_bash_code, string)

def parse_file(filename: str, args: Dict[str, str]={}) -> str:
    with open(filename, 'r') as file:
        data = file.read()
    
    for k, v in args.items():
        data = data.replace('{'+k+'}', str(v))

    return parse(data)

def raw_file_contents(file_path: str) -> Tuple[Dict[str, str], bytes]:
    mime_type, _ = mimetypes.guess_type('.' + file_path)

    if not mime_type:
        mime_type = 'text/plain'

    with open(file_path, 'rb') as f:
        data = f.read()

    return {'Content-Type': mime_type}, data


def remove_html_tags(input_string: str) -> str:
    cleaned_string = bleach.clean(input_string, tags=[], attributes={})
    return cleaned_string 

def error_page(code: int) -> Response:
    type = ResponseCode(code)
    return Response(
        type, 
        {'Content-Type': 'text/html'},
        parse(f'''
        <html>
            <head>
                <style>$[cat style.css]</style>
            </head>
            <body>
                <h1>{type.code}</h1>
                <p>{type.message}</p>
            </body>
        </html>
        ''').encode('utf-8')
    )

def page(title, body): 
    return parse("""         
        <html>
            <head>
                <title>""" + title + """</title>
                <style>$[cat style.css]</style>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
                $[include html/header.html]
                <main>
                    """  + body + """
                </main>
                $[include html/footer.html]
            <body>
        </html>
    """).encode('utf-8')
