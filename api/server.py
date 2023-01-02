from api.urls import url_handlers
from api.models import s

def app(environ, start_response):
    data = url_handlers(environ)
    start_response(
        f"200 OK", [
            ("Content-Type", 'text/html'),
            ("Content-Type", str(len(data))),
        ]
    )
    s.close()
    return iter([data])
