# -*- coding=utf-8 -*-
r"""

"""

import re
import socket
import typing as t


ServerInformationRaw = t.Union[str, int, t.Tuple[t.Optional[str], t.Optional[int]], None]

RE_INET = re.compile(r"(?:inet://)?(?P<host>\w+)(?P<port>:\d+)?")
RE_UNIX = re.compile(r"(?:unix|uds)://(?P<path>\w+)")


def extract_server_info(info: ServerInformationRaw):
    r"""
    None
    <port>
    (<host>, <port>)
    "<host>"
    "<host>:<port>"
    "inet://<host>:<port>"
    "uds://<host>:<port>"
    """
    if info is None:
        return socket.AF_INET, ("", 8000)
    elif isinstance(info, int):
        return socket.AF_INET, ("", info)
    elif isinstance(info, tuple) and len(info) == 2:
        host, port = info
        return socket.AF_INET, (host or "", port or 8000)
    elif isinstance(info, str):
        inet = RE_INET.fullmatch(info)
        if inet is not None:
            return socket.AF_INET, (inet.group("host"), int(inet.group("port")))
        unix = RE_UNIX.fullmatch(info)
        if unix:
            return socket.AF_UNIX, (unix.group("host"), int(unix.group("port")))

    raise ValueError(info)
