import cgi

from models import User

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

def user_list(environ, user, session):
    method = environ.get('REQUEST_METHOD').upper()
    print(environ.get('REQUEST_METHOD'))
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
        # Create a user
        user.email = form['user_email'].value
        print(user)
        session.add(user)
        session.commit()

        return render_template(
            template_name='templates/user_list.html',
            context = {'user': user}
        )
    return render_template(
        template_name='templates/user_list.html',
        context={},
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
        context={'user': user}
    )

def not_found_page(environ, path):
    return render_template(
        template_name='templates/404.html',
        context={'path': path}
    )
