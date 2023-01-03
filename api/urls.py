import json

from views import (
    home, user_list,
    update_user,
    not_found_page,
)
from models import User

def url_handlers(environ, session):
    path = environ.get('PATH_INFO')
    method = environ.get('REQUEST_METHOD').upper()
    user = User()
    # TODO: Figure out how to get and then update existing users.
    if path.endswith("/"):
        path = path[:-1]
    # if method == 'GET':
    #     user = session.query(User).get(uuid=)
    if path == '': # index
        data = home(environ)
    elif path == '/users': # user list or create user
        data = user_list(environ, user, session)
    elif path == f'/users/{user.uuid}':
        data = update_user(environ, user, session)
    else:
        data = not_found_page(environ, path=path)
    # for k, v in environ.items():
    #     print(k, v)

    data = data.encode("utf-8")
    
    return data
