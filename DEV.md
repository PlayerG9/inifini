# General notes

- [WSGI - Web Server Gateways Interface](https://peps.python.org/pep-3333/)
  - want or want not?
- better-exceptions
  - `pip install inifini[development]`
    - server and frontend reloading here?
- msgpack
  - `pip install inifini[msgpack]`

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
    
    def route(self, method: str, endpoint: str): ...
    def GET(self, endpoint: str): ...
    def POST(self, endpoint: str): ...
    def HEAD(self, endpoint: str): ...
    def PUT(self, endpoint: str): ...
    def DELETE(self, endpoint: str): ...
```
