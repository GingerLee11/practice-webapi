import json

from api.handlers import (
    index
)
from api.models import User

def url_handlers(enviorn, start_response, user: User):
    path = enviorn.get('PATH_INFO')
    if path.endswith('/'):
        path = path[:-1]

    if path == '':
        context = index(enviorn)
        if context.get('data'):
            data = json.dumps(context.get('data'))
        else:
            json.dumps(context.get("error"))
        status = context['status']

    data = data.encode('utf-8')

    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Lenth', str(len(data))),
    ]
    start_response(status, response_headers)
    return data