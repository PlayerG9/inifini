# -*- coding=utf-8 -*-
r"""

"""
import os
import typing as t
from io import UnsupportedOperation, DEFAULT_BUFFER_SIZE
from ._base import ResponseBase
from ._kit import RangeSupport


class IOResponse(ResponseBase, RangeSupport):
    _stream: t.IO
    _blksize: t.Optional[int]

    def __init__(self, stream: t.IO, *, blksize: t.Optional[int] = None, auto_close: bool = True):
        if not stream.readable():
            raise UnsupportedOperation("not readable")
        self._stream = stream
        self._blksize = DEFAULT_BUFFER_SIZE if blksize == 1 else blksize
        self.auto_close = auto_close

    def __del__(self):
        if self.auto_close and hasattr(self._stream, 'closed') and not self._stream.closed:
            self._stream.close()

    @property
    def length(self) -> t.Optional[int]:
        if not self._stream.seekable():
            return None
        pos = self._stream.tell()
        end = self._stream.seek(pos, os.SEEK_END)
        self._stream.seek(pos)
        return end

    # @cgi.util.FileWrapper inspired

    def __iter__(self):
        if self._blksize:
            yield from self._stream  # yield lines or so
        else:
            return self  # use __next__

    def __next__(self):
        data = self._stream.read(self._blksize)
        if data:
            return data
        raise StopIteration
