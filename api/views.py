import cgi
from uuid import uuid4
import json

from models import User

def render_template(template_name, context={}):
    html_str = ""
    with open(template_name, 'r') as f:
        html_str = f.read()
        html_str = html_str.format(**context)

        # status = context['status']
        #data = html_str.encode("utf-8")
        # content_type = 'application/json' if int(status.split(' ')[0]) < 400 else 'text/plain'
        # response_headers = [('Content-Type', content_type), ('Content-Length', str(len(data)))]
    return html_str

def home(environ):
    return render_template(
        template_name='templates/index.html',
        context={
            'status': '200 OK'
            }
    )

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
            return render_template(
                template_name='templates/user_list.html',
                context={
                    'error': error,
                    'status': '409 Conflict',
                }
            )
        # Create a user
        user = User()
        user.email = form['user_email'].value
        user.uuid = str(uuid4()).replace('-', '')
        print(user)
        session.add(user)
        session.commit()
        session.close()

        return render_template(
            template_name='templates/user_list.html',
            context = {
                'user': user,
                'status': '200 OK',
            }
        )
    return render_template(
        template_name='templates/user_list.html',
        context={
            'users': users,
            'status': '200 OK',
        },
    )

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

    return render_template(
        template_name='templates/update_user.html',
        context={
            'user': user,
            'status': '302',    
        }
    )

def not_found_page(environ, path):
    return render_template(
        template_name='templates/404.html',
        context={
            'path': path,
            'status': '404 Not Found'
        
        }
    )
