from api.views import (
    home, user_list, add_user, 
    update_user,
    not_found_page,
)

def url_handlers(environ):
    path = environ.get('PATH_INFO')
    if path.endswith("/"):
        path = path[:-1]
    if path == '': # index
        data = home(environ)
    elif path == '/users': # user list or create user
        data = user_list(environ)
    elif path == '/users/update':
        data = update_user(environ)
    else:
        data = not_found_page(environ, path=path)
    # for k, v in environ.items():
    #     print(k, v)
    data = data.encode("utf-8")
    return data
