from templates.route import get_route_to_view


def application(environ, start_response):
    code_response, html_file = get_response(environ)
    start_response(*code_response)
    return html_file


def get_response(environ):
    request_uri = environ.get('REQUEST_URI')
    response, page_body = get_html_response(request_uri)
    return response, page_body


def get_html_response(request_uri):
    try:
        html_response = get_route_to_view(request_uri)
        print(html_response)
        with open(file=html_response, mode='rb') as html:
            html_file = html.read()
        return ('200 OK', [('Content-Type', 'text/html'), ]), html_file
    except FileNotFoundError:
        return ('404', [('Content-Type', 'text/html')]), []
