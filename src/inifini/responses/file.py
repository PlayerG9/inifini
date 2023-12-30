# -*- coding=utf-8 -*-
r"""

"""
import os
import typing as t
from .io import IOResponse


__all__ = ['FileResponse']


class FileResponse(IOResponse):
    def __init__(self, file: t.Union[str, os.PathLike]):
        super().__init__(open(os.fspath(file)))
