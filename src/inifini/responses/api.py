# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from .plain import PlainResponse
try:
    import orjson as json
except ModuleNotFoundError:
    import json
try:
    import msgpack
except ModuleNotFoundError:
    msgpack = None


__all__ = ['ApiResponse']


class ApiResponse(PlainResponse):
    def __init__(self, body: t.Union[dict, list]):
        super().__init__(json.dumps(body))
