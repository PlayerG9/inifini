# -*- coding=utf-8 -*-
r"""

"""
import select
import socket
import threading
import typing as t
from ._util import extract_server_info


class ProductionServer:
    _shutdown_requested: bool
    _is_shut_down: threading.Event

    _threads: t.List[threading.Thread]

    def __init__(self, server_info=None, *, initial_timeout: float = None):
        family, address = extract_server_info(server_info)
        self._socket = socket.socket(family, socket.SOCK_STREAM)
        self._address = address

        self._shutdown_requested = False
        self._is_shut_down = threading.Event()

        self._threads = []

    def run(self, app):
        self.bind()
        try:
            self.serve_forever(app)
        finally:
            self.close()

    def bind(self) -> None:
        self._socket.bind(self._address)
        self._socket.listen()

    def close(self) -> None:
        self._socket.close()

    def serve_forever(self, app) -> None:
        self._shutdown_requested = False
        self._is_shut_down.clear()
        try:
            while not self._shutdown_requested:
                available, *_ = select.select([self._socket], [], [], 0.25)
                # bpo-35017: shutdown() called during select(), exit immediately.
                if self._shutdown_requested:
                    break
                if available:
                    self._handle_new_connection(app=app)
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

            while rfile.readline() != b'\r\n':
                pass

            headers_sent = False

            def start_response(status: str, headers: list):
                nonlocal headers_sent
                wfile.write(f"HTTP/0.9 {status}\r\n".encode())
                for key, value in headers:
                    wfile.write(f"{key}: {value}\r\n".encode())
                wfile.write(b'\r\n')
                headers_sent = True

            response = app({}, start_response)
            for chunk in response:
                if not headers_sent:
                    raise RuntimeError("Headers not sent")
                if isinstance(chunk, str):
                    chunk = chunk.encode()
                wfile.write(chunk)

            print("Closing Connection")
            connection.close()

        thread = threading.Thread(target=_handle)
        self._threads.append(thread)
        thread.start()
