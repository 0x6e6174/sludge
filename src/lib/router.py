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
            log.error(traceback.format_exc())
            return error_page(500)

    def matches(self, request: 'Request') -> bool:
        if not self.method_is_allowed(request.method): return False
        return self.matcher(request.path)

routes = [
    Route(
        lambda request: request.path == '/style.css',
        [Method.GET],
        lambda request, *_: Response(
            ResponseCode.OK, 
            *raw_file_contents('./style.css')
        )
    ),
    Route(
        lambda request: request.path == '/', 
        [Method.GET, Method.POST], 
        lambda request, *_: Response(
            ResponseCode.OK,
            {'Content-Type': 'text/html'},
            (parse_file('./home.html', dict(prev='\\/')).encode('utf-8') if request.method == Method.GET else (
                [
                    (lambda form_data: ( 
                        (lambda time: (
                            f:=open(f'./files/posts-to-homepage/post_{time}.txt', 'w'),
                            f.write(f"<i style='font-family: MapleMonoItalic'>{form_data['name']}</i>@{time}<br>{form_data['text']}<br><br>"),
                            f.close()
                        ))(datetime.now().strftime('%Y-%m-%d_%H:%M:%S-%f')[:-3]) if set(form_data.keys()) == set(['text', 'name']) else None
                    ))(
                    reduce(
                        lambda acc, d: acc.update(d) or acc, 
                        map(lambda key_value_pair: {key_value_pair[0]: remove_html_tags(key_value_pair[1])}, request.body.data.items()), 
                        {}
                    )), 
                    parse_file('./home.html').encode('utf-8')
                ][1]
            ))
        ) if len(request.body.data) > 0 or request.method != Method.POST else error_page(400)
    ),
    Route(
        lambda path: os.path.isdir('.' + path.path), 
        [Method.GET],
        lambda request, *_: Response(
            ResponseCode.OK, 
            {'Content-Type': 'text/html'},
            parse_file('./dir_index.html', dict(path='.' + request.path.path, prev=request.headers.get('Referer').replace('/', '\\/') if request.headers.has('Referer') else '')).encode('utf-8')
        )
    ),
    Route(
        lambda path: os.path.isfile('.' + path.path) and path.path.startswith('/html/') and (path.path.endswith('.html') or '/thoughts/' in path.path),
        [Method.GET],
        lambda request, *_: [print(request.path), Response(
            ResponseCode.OK,
            {'Content-Type': 'text/html'},
            parse_file('.' + request.path.path, dict((k, v.replace('\'', '')) for k, v in map(lambda item: (item[0], item[1]), request.path.params.items()))).encode('utf-8')
        )][-1]
    ), 
    Route(
        lambda path: os.path.isfile('.' + path.path) and (path.path.startswith('/font/') or path.path.startswith('/files/')),
        [Method.GET],
        lambda request, *_: Response(
            ResponseCode.OK,
            *raw_file_contents('.' + request.path.path)
        )
    ),
    Route(
        lambda request: request.path == '/status',
        [Method.GET],
        lambda *_: Response(
            ResponseCode.OK, 
            {'Content-Type': 'text/html'},
            parse('<style>$[cat style.css]</style>$[neofetch | ansi2html]').encode('utf-8')
        )
    ),
    Route(
        lambda request: request.path == '/stats/is-its-computer-online',
        [Method.GET],
        lambda *_: Response(
            ResponseCode.OK,
            {'Content-Type': 'text/html'},
            page("online-p", """
                seconds since last heartbeat message (less than 60: online; less than 120: maybe; more than 120: probably not): $[echo $(( $(date +%s) - $(stat -c %Y ./files/stats/heartbeat) ))]
            """)
        )
    ),
    Route(
        lambda request: request.path == '/stats/what-song-is-it-listening-to', 
        [Method.GET],
        lambda *_: Response( 
            ResponseCode.OK,
            {'Content-type': 'text/html'},
            page("song?", """
                it is listening to $[cat ./files/stats/song] as of $[echo $(( $(date +%s) - $(stat -c %Y ./files/stats/song) ))] seconds ago.
            """)
        )
    ),
    Route(
        lambda request: request.path == '/stats/is-this-server-online', 
        [Method.GET],
        lambda *_: Response( 
            ResponseCode.OK,
            {'Content-type': 'text/html'},
            page("server online-p", """
                I think so.
            """)
        )
    ),
    Route(
        lambda request: request.path == '/stats/what-is-its-servers-uptime', 
        [Method.GET],
        lambda *_: Response( 
            ResponseCode.OK,
            {'Content-type': 'text/html'},
            page("uptime", """
                $[uptime]
            """)
        )
    ),
    Route(
        lambda request: request.path == '/stats/what-vim-buffers-does-it-have-open', 
        [Method.GET],
        lambda *_: Response( 
            ResponseCode.OK,
            {'Content-type': 'text/html'},
            page("vim bufs", """
                $[cat ./files/stats/vim-bufs | xargs -I% echo %'<br>']
            """)
        )
    ),
    Route(
        lambda request: request.path == '/stats',
        [Method.GET],
        lambda request, *_: Response(
            ResponseCode.OK,
            {'Content-Type': 'text/html'},
            parse_file('./html/stats.html', dict(prev=request.headers.get('Referer').replace('/', '\\/') if request.headers.has('Referer') else '')).encode('utf-8')
        )
    ),
    Route(
        lambda _: True,
        [Method.GET],
        lambda *_: error_page(404)
    )
]

