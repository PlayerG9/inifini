# -*- coding=utf-8 -*-
r"""

"""
import typing as t
from ..core.classes import Route


class RouterBase:
    _routes: t.List[Route] = []

    @property
    def routes(self):
        return self._routes

    @t.final
    def add_route(self, route: Route):
        self._routes.append(route)
