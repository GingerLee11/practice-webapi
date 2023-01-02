import os 
print(os.getcwd())

import cgi, types
from json import loads, dumps
from copy import deepcopy
from urllib import parse as urlparse

from gevent.pywsgi import WSGIServer
import gevent

from urls import url_handlers
from models import s

def parseAndDelistArguments(args): 
	if type(args) in [types.StringType, types.UnicodeType] and args[:1] in ['{', '[']:
		args = loads(args)
		if type(args) in [types.ListType, types.ListType]: return args;
	else:
		args = urlparse.parse_qs(args)

	return delistArguments(args)


def delistArguments(args):
	'''
		Takes a dictionary, 'args' and de-lists any single-item lists then
		returns the resulting dictionary.
		{'foo': ['bar']} would become {'foo': 'bar'}
	'''
	
	def flatten(k,v):
		if len(v) == 1 and type(v) is types.ListType: return (str(k), v[0]);
		return (str(k), v)

	return dict([flatten(k,v) for k,v in args.items()])


def app(env, start_response):
    response = url_handlers(env)
    start_response(
        f"200 OK", [
            ("Content-Type", 'text/html'),
            ("Content-Type", str(len(response))),
        ]
    )
    s.close()
    return iter([response])


if __name__ == '__main__':
	wsgi_port = 9000
	print('serving on %s...' % wsgi_port)
	WSGIServer(('', wsgi_port), app).serve_forever()
