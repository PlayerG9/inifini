# -*- coding=utf-8 -*-
r"""

"""
import typing as t


class Route:
    def __init__(self, handler: t.Callable, methods: t.List[str]):
        self._handler = handler
        self._methods = set(methods)

    def __call__(self, *args, **kwargs):
        return self._handler(*args, **kwargs)
