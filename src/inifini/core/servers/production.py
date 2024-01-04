# -*- coding=utf-8 -*-
r"""
todo: TRACE /... HTTP/1.0
"""
import os
import select
import socket
import threading
import typing as t
from ._util import extract_server_info


class ProductionServer:
    _shutdown_requested: bool
    _is_shut_down: threading.Event

    _threads: t.List[threading.Thread]

    max_line_length: t.ClassVar[int] = 2**16

    def __init__(self, server_info=None, *, cycle_timeout: float = None, initial_timeout: float = None):
        family, address = extract_server_info(server_info)
        self._socket = socket.socket(family, socket.SOCK_STREAM)
        self._address = address

        self._shutdown_requested = False
        self._is_shut_down = threading.Event()

        self._cycle_timeout = cycle_timeout

        self._threads = []

    def run(self, app):
        self.bind()
        try:
            self.serve_forever(app)
        except KeyboardInterrupt:
            for thread in self._threads:
                thread.join()
        finally:
            self.close()

    def bind(self) -> None:
        self._socket.bind(self._address)
        self._socket.listen()
        host, port = self._socket.getsockname()
        print(f"Bound to {host}:{port}")  # todo: replace with proper event logging

    def close(self) -> None:
        self._socket.close()

    def serve_forever(self, app) -> None:
        self._shutdown_requested = False
        self._is_shut_down.clear()
        app_interval = getattr(app, "_interval", None)  # todo: better name
        timeout = self._cycle_timeout or 0.25
        try:
            while not self._shutdown_requested:
                available, *_ = select.select([self._socket], [], [], timeout)
                # bpo-35017: shutdown() called during select(), exit immediately.
                if self._shutdown_requested:
                    break
                if available:
                    self._handle_new_connection(app=app)
                if app_interval:
                    app_interval()
        finally:
            self._shutdown_requested = False
            self._is_shut_down.set()

    def shutdown(self, gracefully: bool = True) -> None:
        r"""
        breaks the serve_forever()

        :param gracefully: wait for all handlers to stop
        """
        self._shutdown_requested = True
        self._is_shut_down.wait()
        if gracefully:
            for thread in self._threads:
                thread.join()

    def _handle_new_connection(self, app):
        connection, address = self._socket.accept()
        print("New Connection from", address)

        def _handle():
            rfile = connection.makefile('rb')
            wfile = connection.makefile('wb')

            first_line = rfile.readline(self.max_line_length).decode()
            if len(first_line) >= self.max_line_length or first_line.count(' ') != 2:
                wfile.write(b'HTTP/1.0 400 Bad Request')  # maybe more later
                connection.close()
                return
            method, uri, http_version = first_line.split(' ')

            path_info, sep, query_string = uri.partition('?')

            server_name, server_port = self._socket.getsockname()

            environ = {
                'wsgi.input': rfile,
                'wsgi.errors': open(os.devnull, 'w'),  # todo: bad to discard all
                'wsgi.version': (1, 0),
                'wsgi.multithread': True,
                'wsgi.multiprocess': False,
                'wsgi.run_once': False,
                'wsgi.url_scheme': "http",
                'REQUEST_METHOD': method,
                'SCRIPT_NAME': "",  # root-path  # todo
                'PATH_INFO': path_info or '/',
                'QUERY_STRING': query_string or "",
                'SERVER_NAME': server_name,
                'SERVER_PORT': server_port,
                'SERVER_PROTOCOL': "HTTP/1.0"
            }

            headers_set: list = []
            headers_sent: list = []

            def write(data: t.AnyStr):
                if not headers_set:
                    raise AssertionError("write() called before start_response()")
                elif not headers_sent:
                    status, headers = headers_sent[:] = headers_set
                    wfile.write(f"HTTP/1.0 {status}\r\n".encode())
                    for key, value in headers:
                        wfile.write(f"{key}: {value}\r\n".encode())
                    wfile.write(b'\r\n')

                if isinstance(data, str):
                    data = data.encode()
                wfile.write(data)
                wfile.flush()

            def start_response(status: str, headers: list, exc_info=None):
                if exc_info:  # if an exception occurred it's allowed to change headers if not sent
                    try:
                        if headers_sent:
                            # Re-raise original exception if headers sent
                            raise exc_info[1].with_traceback(exc_info[2])
                    finally:
                        exc_info = None  # noqa: Avoid circular ref
                elif headers_set:
                    raise AssertionError("Headers already set!")

                headers_set[:] = [status, headers]

                return write

            response = app(environ, start_response)
            if response is not None:  # from start_response() returned write() used
                try:
                    for chunk in response:
                        write(chunk)
                finally:
                    if hasattr(response, 'close'):
                        response.close()
            elif not headers_sent:
                raise AssertionError("Nothing sent")

            connection.close()

        thread = threading.Thread(target=_handle)
        self._threads.append(thread)
        thread.start()
