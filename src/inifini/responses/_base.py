# -*- coding=utf-8 -*-
r"""

"""
import typing as t


__all__ = ['ResponseBase']


class ResponseBase:
    @property
    def headers(self) -> None:
        return None

    @property
    def length(self) -> t.Optional[int]:
        return None

    def __iter__(self) -> t.Iterable[bytes]:
        raise NotImplementedError()
