# General notes

- [WSGI - Web Server Gateways Interface](https://peps.python.org/pep-3333/)
  - want or want not?
- better-exceptions
  - `pip install inifini[development]`
    - server and frontend reloading here?
- msgpack
  - `pip install inifini[msgpack]`
- scheduling
  - `pip install inifini[schedule]`/`pip install inifini[tasks]`
  - `schedule`-library‽

# Minification (html/css/js)

- `pip install inifini[minify]`
- `pip install inifini[minify:html]`
- `pip install inifini[minify:css]`
- `pip install inifini[minify:js]`

```python
@route()
def dunno():
    return """</div>
    <h1>Hello World</h1>
</div>"""
```
```html
<div><h1>Hello World</h1></div>
```

# Templating

- `pip install inifini[jinja]`

# Builtin support to be used as an API

```python
@apidoc(hello=str)
@route()
def dunno():
    return {'hello': "World"}
```

ReDoc and Swagger?

- `pip install inifini[api]`

# Server-Reloading

Made in mind with integration for background-threads and workers

- `ast` before reloading to prevent crashes

# Web-Reloading

livereload? or custom


# Notes

## Debugger

separate debugger process which is a terminal UI

new requests get `⟳` which successful ones have status-code with color and fade out over time.

```
14:13:56,4853 | 200 | /home
14:13:56,4870 | ⟳   | /api/resource
14:13:56,4874 | ⟳   | /api/resource
```

## Json serialization/deserialization
- orjson
- ujson
- json (builtin)


# Interfaces

```python
class Router:
    def mount_router(self, router: 'Router', prefix: str = None): ...
    def mount_wsgi(self, wsgi_app, prefix: str = None): ...
    def mount_asgi(self, asgi_app, prefix: str = None): ...
    
    def add_route(self, route: 'Route'): ...
    def route(self, method: str, endpoint: str) -> 'Route': ...
    def GET(self, endpoint: str) -> 'Route': ...
    def POST(self, endpoint: str) -> 'Route': ...
    def HEAD(self, endpoint: str) -> 'Route': ...
    def PUT(self, endpoint: str) -> 'Route': ...
    def DELETE(self, endpoint: str) -> 'Route': ...
```

```python
@GET("/")
def index(context: 'Context'):
    return "Hello World"
```

## ProxyRouter

```python
class ProxyRouter:
    r"""
    re-sends to your frontend written with a JS-Framework and hosted on a different port
    """
    
    def __init__(self, target: str, rewrite: callable): ...
```
```python
app.mount_router(StaticRouter("@web-ui/") if prod else ProxyRouter(target=3000), "/")
```


## Flow

```python
readable, *_ = select.select([sock, *connections])
for conn in readable:
    read_possible(conn)  # read available bytes (max till header-end!?)
    if processable(conn):  # if head was read
        start_thread(conn)  # start thread with route
```


## Dunno

`views/a.py`
```python
from inifini import GET

@GET("/something")
def something(): ...
```
`views/b.py`
```python
from inifini import GET

@GET("/something")
def something(): ...
```

`main.py`
```python
import inifini

app = inifini.Application()
app.load_routes("@views")
```
