import os 
print(os.getcwd())

import cgi, types
from json import loads, dumps
from copy import deepcopy
from urllib import parse as urlparse

from gevent.pywsgi import WSGIServer
import gevent

from urls import url_handlers


def app(env, start_response):
    response = url_handlers(env)
    start_response(
        f"200 OK", [
            ("Content-Type", 'text/html'),
            ("Content-Type", str(len(response))),
        ]
    )
    return iter([response])


if __name__ == '__main__':
	wsgi_port = 9000
	print('serving on %s...' % wsgi_port)
	WSGIServer(('', wsgi_port), app).serve_forever()
