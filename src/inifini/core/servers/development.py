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
        registry.auto_register(filter=self._get_filter())
        # jurigged.watch
        watcher = jurigged.Watcher(registry=registry)
        watcher.start()
        try:
            super().serve_forever(app=app)
        finally:
            watcher.stop()

    @staticmethod
    def _get_filter():
        import sys
        import os.path as p
        import fnmatch

        root = getattr(sys.modules.get('__main__', None), '__file__', ".")
        pattern = p.dirname(p.abspath(root)) + "/*.py"
        print([root, pattern])

        def allowed(filename: str) -> bool:
            return fnmatch.fnmatch(filename, pattern)

        return allowed
