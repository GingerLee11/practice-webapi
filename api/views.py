from api.models import User, users

def render_template(template_name, context={}):
    html_str = ""
    with open(template_name, 'r') as f:
        html_str = f.read()
        html_str = html_str.format(**context)
    return html_str

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

def add_user(environ):
    return render_template(
        template_name='api/add_user.html',
        context={},
    )

def not_found_page(environ, path):
    return render_template(
        template_name='api/404.html',
        context={'path': path}
    )
