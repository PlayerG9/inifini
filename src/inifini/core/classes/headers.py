# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import collections.abc
# from wsgiref.headers import Headers


HeadersInit = t.Union['Headers', t.List[t.Tuple[str, str]], t.Dict[str, str]]


class Headers:
    _headers: t.List[t.Tuple[str, str]]

    def __init__(self, init: HeadersInit = None, **headers):
        self._headers = []
        self.update(init)
        self.update(headers)

    # todo: add support for there _params
    def add_header(self, key: str, value: t.Any, **_params):
        self._headers.append((key, str(value)))

    def replace(self, key: str, value: t.Any):
        self.remove_header(key)
        self.add_header(key, value)

    def get(self, key: str, *, fallback=None):
        pass

    def remove_header(self, key: str):
        pass

    def update(self, val: HeadersInit):
        if val is None:
            return
        if isinstance(val, collections.abc.Mapping):
            for key in val:
                self.add_header(key, val[key])
        elif isinstance(val, collections.Iterable):
            for key, value in val:
                self.add_header(key, value)

    def clear(self):
        self._headers.clear()

    def __contains__(self, item): ...
    def __getitem__(self, item): ...
    def __setitem__(self, key, value): ...
    def __delitem__(self, key): ...
    def __iter__(self): ...
    def __len__(self): ...
    def __or__(self, other): ...
    def __ior__(self, other): ...
