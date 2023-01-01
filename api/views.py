from api.models import User

def render_template(template_name, context={}):
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

def user_list(environ):
    return render_template(
        template_name='templates/user_list.html',
        context={},
    )

def add_user(environ):
    return render_template(
        template_name='templates/add_user.html',
        context={},
    )

def not_found_page(environ, path):
    return render_template(
        template_name='templates/404.html',
        context={'path': path}
    )
