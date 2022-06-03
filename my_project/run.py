from wsgiref.simple_server import make_server
from whitenoise import WhiteNoise

from geek_framework.main import Framework
from urls import fronts
from views import routes

application = Framework(routes, fronts)
application = WhiteNoise(application, root="./static/")

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    print('Поехали http://localhost:8080/')
    httpd.serve_forever()
