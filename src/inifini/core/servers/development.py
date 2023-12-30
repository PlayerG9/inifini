# -*- coding=utf-8 -*-
r"""

"""
from .production import ProductionServer
try:
    from better_exceptions import format_exception
except ModuleNotFoundError:
    from traceback import format_exception
try:
    import jurigged
except ModuleNotFoundError:
    pass


class DevelopmentServer(ProductionServer):
    def serve_forever(self, app) -> None:
        registry = jurigged.register.Registry()
        # jurigged.watch
        watcher = jurigged.Watcher(registry=registry)
        watcher.start()
        try:
            super().serve_forever(app=app)
        finally:
            watcher.stop()
