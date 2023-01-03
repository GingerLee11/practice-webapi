import os 
print(os.getcwd())

from uuid import uuid4
import cgi, types
from json import loads, dumps
from copy import deepcopy
from urllib import parse as urlparse

from gevent.pywsgi import WSGIServer
import gevent

from views import (
    home, user_list,
    update_user,
)
from models import Session, User

def app(env, start_response):
    session = Session()
    path = env.get('PATH_INFO')
    method = env.get('REQUEST_METHOD').upper()
    print(method)
    wsgi_input = env['wsgi.input']
    args = env['QUERY_STRING']
    # TODO: Figure out how to get and then update existing users.
    str_path = str(path).split('/')[-1]
    print(str_path)
    # Check if the UUID correlates to an existing user
    # Otherwise it will be a new user
    qs = session.query(User).filter_by(uuid=str(str_path)).all()
    
    # List of all users
    users = session.query(User).all()
    
    print(qs)
    if qs:
        user = qs[0]
    else:
        user = User()
    status = '200 OK'
    if wsgi_input.content_length and method != 'PUT':
        post_env = env.copy()
        post_env['QUERY_STRING'] = ''
        form = cgi.FieldStorage(
            fp=env['wsgi.input'],
            env=post_env,
            keep_blank_values=True
        )
        form_data = [(k, form[k].value) for k in form.keys()]
        args.update(form_data)
        email = form_data['user_email'].value
    if method == 'PUT':
        wsgi_input = wsgi_input.read()
        args.update(wsgi_input)

    if path == '/favicon.ico': 
        start_response('301 Moved Permanently', [('Location', '')])
        return ''

    if path.endswith("/"):
        path = path[:-1]

    if path == '': # index
        data = home(env)

    elif path == '/users': # user list or create user
        if method == 'POST':
            qs = session.query(User).filter_by(email=email).all()
            if qs:
                status = '409 Conflict'
                error = f'User with {email} already exists.'
            else:
                user.email = email
                user.uuid = str(uuid4()).replace('-', '') + str(uuid4()).replace('-', '')
                print(user)
                session.add(user)
                session.commit()
                status = '201 Created'
        data = user_list(env, users)

    elif path == f'/users/{user.uuid}':
        if method == 'PUT':
            post_env = env.copy()
            post_env['QUERY_STRING'] = ''
            form = cgi.FieldStorage(
                fp=env['wsgi.input'],
                env=post_env,
                keep_blank_values=True
            )
            form_data = [(k, form[k].value) for k in form.keys()]
            print(form_data)
        data = update_user(env, user)
    else:
        status = '404 Not Found'
    if session: 
        session.close()
    response = data.encode("utf-8")
    
    try:
        ret = { 
            'path' : path,
            'args' : args,
            'method' : method,
            'response': response #the output of the functions you call
		}

        start_response(f'{status}', [('Content-Type', 'application/json')])
        return dumps(ret)

    except Exception as inst:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return repr(inst)

    start_response(
        f"{status}", [
            ("Content-Type", 'html/text'),
            ("Content-Length", str(len(response))),
        ]
    )
    return iter([response])


if __name__ == '__main__':
	wsgi_port = 9000
	print('serving on %s...' % wsgi_port)
	WSGIServer(('', wsgi_port), app).serve_forever()
