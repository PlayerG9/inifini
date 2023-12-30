# -*- coding=utf-8 -*-
r"""

"""
import os
import typing as t
from io import UnsupportedOperation
from ._base import ResponseBase
from ._kit import RangeSupport


class IOResponse(ResponseBase, RangeSupport):
    _stream = t.IO

    def __init__(self, stream: t.IO):
        if not stream.readable():
            raise UnsupportedOperation("not readable")
        self._stream = stream

    def __del__(self):
        if not self._stream.closed:
            self._stream.close()

    @property
    def length(self) -> t.Optional[int]:
        if not self._stream.seekable():
            return None
        pos = self._stream.tell()
        end = self._stream.seek(pos, os.SEEK_END)
        self._stream.seek(pos)
        return end

    def __iter__(self):
        yield from self._stream
