import cgi
from uuid import uuid4
import json

from models import User

def render_template(template_name, context):
    html_str = ""
    with open(template_name, 'r') as f:
        html_str = f.read()
        html_str = html_str.format(**context)
    return html_str

def home(environ):
    return render_template(
        template_name='templates/index.html',
        context={}
    )

def user_list(environ, users):
    user_str = ''
    for user in users:
        user_str += f'<li><a href="#">{user.email}</a></li>'
    print(user_str)
    return render_template(
        template_name='templates/user_list.html',
        context={
            'users': user_str,
        }
    )

def update_user(environ, user):
    return render_template(
        template_name='templates/update_user.html',
        context={
            'user': user,
        }
    )

def not_found_page(environ, path):
    return render_template(
        template_name='templates/404.html',
        context={
            'path': path,
        }
    )
