def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Hello world from a simple WSGI application!']

# Установка
# pip install uwsgi

# Запуск
# uwsgi --http :8000 --wsgi-file simple_wsgi_server.py