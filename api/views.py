from api.models import User, users

from api.urls import render_template

def home(environ):
    return render_template(
        template_name='api/index.html',
        context={}
    )

def user_list(environ):
    return render_template(
        template_name='api/user_list.html',
        context={'users': users}
    )
