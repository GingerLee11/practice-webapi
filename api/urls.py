from api.views import (
    home, user_list, add_user, 
    not_found_page
)

def url_handlers(environ):
    path = environ.get('PATH_INFO')
    request_method = environ.get('REQUEST_METHOD')
    if path.endswith("/"):
        path = path[:-1]
    if path == '': # index
        data = home(environ)
    elif path == '/users': # user list or create user
        if request_method == 'GET': 
            data = user_list(environ)
        elif request_method == 'POST':
            data = add_user(environ)            
    else:
        data = not_found_page(environ, path=path)
    for k, v in environ.items():
        print(k, v)
    data = data.encode("utf-8")
    return data
