# -*- coding=utf-8 -*-
r"""

"""
import typing as t


# (status: "200 OK", [(key, value), ...]) -> None
START_RESPONSE = t.Callable[[str, t.Iterable[t.Tuple[str, str]]], None]


class App:
    def __call__(self, environ: dict, start_response: START_RESPONSE):
        print("Hello App")
        start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", "12")])
        print("Yielding Body")
        yield "Hello World!"
