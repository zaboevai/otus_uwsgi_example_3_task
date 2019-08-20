import os

BASE_PATH = './Notebook_shop'


def application(environ, start_response):
    write_last_request_to_file(environ)

    if not environ['REQUEST_METHOD'] == 'GET':
        start_response('404', [('Content-Type', 'text/html')])
        return [f'Методе {environ["REQUEST_METHOD"]} запрос ещё не обрабатывается']

    request_uri = environ['REQUEST_URI']

    html_file = get_html(request_uri)

    if html_file:
        start_response('200 OK', [('Content-Type', 'text/html'), ])
        return [html_file]

    return []


def get_html(file):
    try:

        if file == '/':
            file = 'index.html'
        else:
            file = file[1:]

        if file[-3:] == 'ico':
            return file

        with open(file=os.path.join(BASE_PATH, file), mode='rb') as html:
            html_file = html.read()
        return html_file
    except FileNotFoundError:
        return None


def write_last_request_to_file(environ):
    with open(file='last_request.log', mode='w') as log:
        for k, v in environ.items():
            log.write(f'{k}: {v} \n')

#
# if __name__ == '__main__':
#     try:
#         from wsgiref.simple_server import make_server
#         httpd = make_server('', 8000, application)
#         print('Serving on port 8000...')
#         httpd.serve_forever()
#     except KeyboardInterrupt:
#         print('Goodbye.')
