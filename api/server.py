# Gunicorn

def render_template(template_name='index.html'):
    return '<h1>Hello, World!</h1>'

def app(environ, start_response):
    for k, v in environ.items():
        print(k, v)
    data = render_template()
    data = data.encode("utf-8")
    start_response(
        f"200 OK", [
            ("Content-Type", 'text/html'),
            ("Content-Type", str(len(data))),
        ]
    )
    return iter([data])
