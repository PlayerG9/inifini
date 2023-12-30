# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from ._base import ResponseBase


__all__ = ['PlainResponse']


class PlainResponse(ResponseBase):
    _body: bytes

    def __init__(self, body: t.Union[str, bytes]):
        self._body = body if isinstance(body, bytes) else body.encode()

    @property
    def length(self) -> t.Optional[int]:
        return len(self._body)

    def __iter__(self):
        yield from self._body
