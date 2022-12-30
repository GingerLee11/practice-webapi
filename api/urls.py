# urls.py

def render_template(template_name, context={}):
    html_str = ""
    with open(template_name, 'r') as f:
        html_str = f.read()
        html_str = html_str.format(**context)
    return html_str

def url_handlers(environ):
    pass