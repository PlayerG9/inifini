# -*- coding=utf-8 -*-
r"""

"""
try:
    import orjson as json
except ModuleNotFoundError:
    try:
        import ujson as json
    except ModuleNotFoundError:
        import json

try:
    import msgpack
except ModuleNotFoundError:
    pass
