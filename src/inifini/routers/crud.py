# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from ._base import RouterBase
from ..core.classes import Route


class CRUDRouter(RouterBase):

    @t.overload
    def GET(self, endpoint: t.Callable, path: str) -> t.Callable: ...

    def GET(self, endpoint: t.Callable = None, **kwargs) -> t.Callable[[t.Callable], t.Callable]:
        def decorator(fn: t.Callable) -> t.Callable:
            kwargs.update(method="GET")
            route = Route(handler=fn, **kwargs)
            self.add_route(route)
            return route

        return decorator(endpoint) if endpoint is not None else decorator
