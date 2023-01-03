import cgi
from uuid import uuid4
import json

from models import User


def home(environ):
    return {
        'data': '<h1>Hello, World!</h1>',
        'status': '200 OK'
    }

def user_list(environ, session):
    method = environ.get('REQUEST_METHOD').upper()
    print(environ.get('REQUEST_METHOD'))
    users = session.query(User).all()
    if method == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        form = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=post_env,
            keep_blank_values=True
        )
        form_data = [(k, form[k].value) for k in form.keys()]
        print(form_data)
        # TODO: Check for existing email:
        # If the email is the same go to update instead of creation
        email = form['user_email'].value
        qs = session.query(User).filter_by(email=email).all()
        if qs:
            error = f'User with {email} already exists!'
 
            context={
                'error': error,
                'status': '409 Conflict',
            }
            return context
        # Create a user
        user = User()
        user.email = form['user_email'].value
        user.uuid = str(uuid4()).replace('-', '')
        print(user)
        session.add(user)
        session.commit()
        session.close()
        context = {
            'data': user,
            'status': '201 Created',
        }
        return context
    context = {
        'data': users,
        'status': '200 OK',
    }
    return context

def update_user(environ, user, session):
    method = environ.get('REQUEST_METHOD').upper()
    print(environ.get('REQUEST_METHOD'))
    if method == 'PUT':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        form = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=post_env,
            keep_blank_values=True
        )
        form_data = [(k, form[k].value) for k in form.keys()]
        print(form_data)

    context={
        'data': user,
        'status': '302 Found',    
    }
    return context

def not_found_page(environ, path):
    context={
        'data': path,
        'status': '404 Not Found'
    }
    return context
