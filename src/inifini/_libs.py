# -*- coding=utf-8 -*-
r"""

"""
# get the fastest available json library with builtin-json as fallback
# orjson > ujson > json
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
    msgpack = None
