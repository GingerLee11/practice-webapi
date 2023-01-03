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
    update_user, not_found_page,

)
from models import Session, User, send_python_email

def app(env, start_response):
    session = Session()
    # for k, v in env.items():
    #     print(k, v)
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
            environ=post_env,
            keep_blank_values=True
        )
        form_data = [(k, form[k].value) for k in form.keys()]
        # args.update(form_data)
        email = form['user_email'].value
    if method == 'PUT':
        wsgi_input = wsgi_input.read()
        # args.update(wsgi_input)

    if path == '/favicon.ico': 
        start_response('301 Moved Permanently', [('Location', '')])
        return ''

    if path.endswith("/"):
        path = path[:-1]

    print(path)
    if path == '': # index
        response = home(env)

    elif path == '/users': # user list or create user
        if method == 'POST':
            qs = session.query(User).filter_by(email=email).all()
            if qs:
                status = '409 Conflict'
                error = f'User with {email} already exists.'
            else:
                user.email = email
                user.uuid = str(uuid4()).replace('-', '') + str(uuid4()).replace('-', '')
                
                # Send email with link containing the uuid
                url = env['HTTP_HOST']
                uri = env['PATH_INFO']
                message = f"Click this link to login: {url}{uri}/{user.uuid}"
                print(message)
                send_python_email(email, message)

                print(user)
                session.add(user)
                session.commit()
                status = '201 Created'
        response = user_list(env, users)

    elif path == f'/users/{str(user.uuid)}':
        if method == 'PUT':
            post_env = env.copy()
            post_env['QUERY_STRING'] = ''
            form = cgi.FieldStorage(
                fp=env['wsgi.input'],
                environ=post_env,
                keep_blank_values=True
            )
            form_data = [(k, form[k].value) for k in form.keys()]
            print(form_data)
        response = update_user(env, user)
    else:
        response = not_found_page(env, path)
        status = '404 Not Found'
    if session: 
        session.close()
    response = response.encode("utf-8")
    print(f'type: {type(response)}')

    start_response(
        f"{status}", [
            ("Content-Type", 'text/html'),
            ("Content-Length", str(len(response))),
        ]
    )
    return iter([response])


if __name__ == '__main__':
	wsgi_port = 9000
	print('serving on %s...' % wsgi_port)
	WSGIServer(('', wsgi_port), app).serve_forever()
