# Demo: HTTP persistent connection breakage when using h2c in gevent

This repository contains a minimum runnable example demonstrating an issue with
HTTP/1.1 persistent connections if a client tries to connect using the h2c protocol.

The problem is, that an HTTP/2 Cleartext (h2c) upgrade request is an HTTP/1.1 request,
which contains `Connection: Upgrade` and `Upgrade: h2c` headers. `gevent` does not
support HTTP/2 by now, but as this request is a HTTP/1.1 request, it must be handled by
gevent.

gevent currently does handle this case correctly, because it uses the `Connection`
header to determine, whether its a `websocket` upgrade request or not, which
(on its own) is not correct. In this case, the logic passes the wrong buffer to the
application as `wsgi.input`, which results in the internal logic discarding parts of the
next request after the first one has been handled.

This can be seen in [`gevent.pywsgi._connection_upgrade_requested`](https://github.com/gevent/gevent/blob/a67891991c95b5ffca78dc1f1a11f956ec3963ca/src/gevent/pywsgi.py#L814)
which is used in [`gevent.pyswgi.WSGIServer.get_environ`](https://github.com/gevent/gevent/blob/a67891991c95b5ffca78dc1f1a11f956ec3963ca/src/gevent/pywsgi.py#L1279)
to determine whether to pass an `gevent.pywsgi.Input` object to the application of the
buffer directly.

In [`gevent.pywsgi.handle_one_response`](https://github.com/gevent/gevent/blob/a67891991c95b5ffca78dc1f1a11f956ec3963ca/src/gevent/pywsgi.py#L1110)
the "remaining" contents of the buffer are then discarded, which results in the next
request being read from the buffer, because the `gevent.pywsgi.Input` object, being
out-of-sync with the underlying buffer.


## Usage

This demo can be started quite easly. You only require a python virtual environment and
two shells.

First, clone this repository and create the virtual environment and install the
requirements:

```shell
> git clone https://github.com/hansingt/gevent_h2c_issue.git
> cd gevent_upgrade_issue
> python -m venv venv
> ./venv/bin/pip install -r requirements.txt
```

Then, in one shell, start the server:

```shell
> ./venv/bin/python server.py
```

And in another shell start the client:

```shell
> ./venv/bin/python client.py
```
