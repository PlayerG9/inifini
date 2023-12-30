# -*- coding=utf-8 -*-
r"""

"""
from collections.abc import Mapping
from .path import Path


class PathVars(Mapping):
    def __init__(self, path: str, **variables):
        self._path = Path(path)
        self._variables = variables

    def __repr__(self):
        return f"<{type(self).__name__} {self._path}>"

    def __str__(self):
        return self._path.format(self._variables)

    # abstract mapping methods

    def __len__(self):
        return len(self._variables)

    def __iter__(self):
        yield from self._variables

    def __getitem__(self, __key):
        return self._variables[__key]
