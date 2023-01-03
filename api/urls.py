import json

from views import (
    home, user_list,
    update_user,
    not_found_page,
)
from models import User, Session

def url_handlers(environ, start_response):
    session = Session()
    path = environ.get('PATH_INFO')
    method = environ.get('REQUEST_METHOD').upper()

    # TODO: Figure out how to get and then update existing users.
    str_path = str(path).split('/')[-1]
    print(str_path)
    qs = session.query(User).filter_by(uuid=str(str_path)).all()
    print(qs)
    if qs:
        user = qs[0]
    else:
        user = User()
    if path == '/favicon.ico': 
        start_response('301 Moved Permanently', [('Location', '')])
        return ''

    if path.endswith("/"):
        path = path[:-1]

    if path == '': # index
        data = home(environ)
    elif path == '/users': # user list or create user
        data = user_list(environ, session)
    elif path == f'/users/{user.uuid}':
        data = update_user(environ, user, session)
    else:
        data = not_found_page(environ, path=path)
    # for k, v in environ.items():
    #     print(k, v)
    # status = context['status']
    data = data.encode("utf-8")
    # content_type = 'application/json' if int(status.split(' ')[0]) < 400 else 'text/plain'
    # response_headers = [('Content-Type', content_type), ('Content-Length', str(len(data)))]
    if session:
        session.close()
    # start_response(status, response_headers)
    return data
