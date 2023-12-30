# -*- coding=utf-8 -*-
r"""

"""
import typing as t
import dataclasses
from functools import cached_property


@dataclasses.dataclass(frozen=True, kw_only=True)
class Request:
    method: str
    path: str
    headers: t.List[t.Tuple[str, str]]
    body: t.Optional[str]

    @cached_property
    def body_as_json(self) -> t.Any:
        from ..._libs import json
        if self.body is None:
            raise ValueError("missing body. can't load json")
        return json.loads(self.body)
