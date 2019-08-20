import os

VIEWS_BASE_PATH = './views'

ROUTES_TO_VIEWS = {'/': 'index.html',
                   '/index': 'index.html',
                   '/home': 'index.html',
                   '/favicon.ico': 'favicon.ico',
                   '/contacts': 'contacts.html',
                   '/catalog': 'catalog.html',
                   '/content/mi_air': 'content/mi_air.html',
                   '/content/lenovo_330': 'content/lenovo_330.html',
                   '/img/mi_air_laptop': 'img/mi_air_laptop.jpg',
                   '/img/lenovo_330': 'img/lenovo_330.jpg',
                   }


def get_route_to_view(route):
    try:
        view = ROUTES_TO_VIEWS[route]
    except KeyError as exc:
        raise exc

    return os.path.join(VIEWS_BASE_PATH, view)
