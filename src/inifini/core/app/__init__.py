# -*- coding=utf-8 -*-
r"""

"""
import typing as t
if t.TYPE_CHECKING:
    import schedule


# (status: "200 OK", [(key, value), ...]) -> None
START_RESPONSE = t.Callable[[str, t.Iterable[t.Tuple[str, str]]], None]


class Application:
    _endpoint = lambda: "Hello Endpoint"

    def __call__(self, environ: dict, start_response: START_RESPONSE):
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ: dict, start_response: t.Callable) -> t.Any:
        message = self._endpoint()
        start_response("200 OK", [("Content-Type", "text/plain"), ("Content-Length", len(message))])
        yield message

    def get(self):
        def decorator(fn):
            self._endpoint = fn
            return fn
        return decorator

    _scheduler: 'schedule.Scheduler' = None

    @property
    def scheduler(self) -> 'schedule.Scheduler':
        import schedule
        self._scheduler = schedule.Scheduler()
        return self._scheduler

    def every(self, interval: int = 1) -> 'schedule.Job':
        r"""
        shortcut for app.scheduler.every()
        """
        return self.scheduler.every(interval=interval)

    def _iteration(self):
        if self._scheduler is not None:
            self.scheduler.run_pending()
