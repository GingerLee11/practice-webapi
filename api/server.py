from api.views import (
    home, user_list
)
from api.urls import render_template

def app(environ, start_response):
    path = environ.get('PATH_INFO')
    if path.endswith("/"):
        path = path[:-1]
    if path == '': # index
        data = home(environ)
    elif path == '/users': # user list
        data = user_list(environ)
    else:
        data = render_template(template_name='api/404.html', context={"path": path})
    for k, v in environ.items():
        print(k, v)
    data = data.encode("utf-8")
    start_response(
        f"200 OK", [
            ("Content-Type", 'text/html'),
            ("Content-Type", str(len(data))),
        ]
    )
    return iter([data])
