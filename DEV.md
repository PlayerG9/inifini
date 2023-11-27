# General notes

- [WSGI - Web Server Gateways Interface](https://peps.python.org/pep-3333/)
  - want or want not?
- msgpack
  - `pip install inifini[msgpack]`
- better-exceptions
  - `pip install inifini[development]`
    - server and frontend reloading here?

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

# Templating

- `pip install inifini[jinja]`
