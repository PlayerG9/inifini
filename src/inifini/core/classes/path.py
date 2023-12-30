# -*- coding=utf-8 -*-
r"""

"""
import re


class Path:
    def __init__(self, raw: str):
        self._raw = raw
        self._regex = re.compile(r"")

    def __repr__(self):
        return f"<{type(self).__name__} {self._raw!r}>"

    def parameters(self):
        pass

    def format(self, __variables: dict = None, **variables):
        variables = (__variables or {}) | variables
        return self._raw
