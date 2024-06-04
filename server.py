#!/venv/bin/python
"""
Example gevent WSGI server demonstrating the breakage of the HTTP persistent connections
when a client tries to connect using HTTP/2.

This is a very simple "Hello World" WSGI server based on the `gevent.pywsgi.WSGIServer`.

It can be started using a python virtualenvironment containing the `gevent` package:

```bash
> python -m venv venv
> ./venv/bin/python -m pip install -r requirements.txt
> ./venv/bin/python server.py
```
"""
import logging
import socket
from typing import Iterable
from wsgiref.types import StartResponse, WSGIEnvironment
from gevent.pywsgi import WSGIServer



class FastWSGIServer(WSGIServer):
    def init_socket(self) -> None:
        super().init_socket()
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)


def echo(
    environ: WSGIEnvironment,
    start_response: StartResponse,
) -> Iterable[bytes]:
    """Simple, long running, "echo" WSGI application."""
    content_length = int(environ["CONTENT_LENGTH"])
    msg = environ["wsgi.input"].read(content_length)
    start_response("200", [])
    return [msg]


server = FastWSGIServer(
    listener=("127.0.0.1", 8080),
    backlog=None,
    application=echo,
    log=logging.getLogger("access"),
    error_log=logging.getLogger("errors"),
)
server.serve_forever()
