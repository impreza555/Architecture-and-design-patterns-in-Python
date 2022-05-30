from quopri import decodestring
from geek_framework.requests import GetRequests, PostRequests
from views import NotFound404


class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        """
        Инициализация фреймворка
        :param routes_obj: dict - словарь соответствия маршрутов
        :param fronts_obj: list - список методов фронт контроллера
        """
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        """
        Вызов фреймворка
        :param environ: dict - словарь данных от сервера
        :param start_response: function - функция для ответа серверу
        :return:
        """
        request = {}
        path = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']
        request['method'] = method
        if not path.endswith('/'):
            path = f'{path}/'
        if method == 'POST':
            post_request = PostRequests(environ)
            data = post_request.post_request_params()
            request['data'] = Framework.decode_value(data)
            print(f'Нам пришёл post-запрос: {Framework.decode_value(data)}')
        if method == 'GET':
            get_request = GetRequests(environ)
            data = get_request.get_request_params()
            request['data'] = Framework.decode_value(data)
            print(f'Нам пришли GET-параметры:'
                  f' {Framework.decode_value(data)}')
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = NotFound404()
        for front in self.fronts_lst:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        """
        Метод декодирования байтового значения в строку.
        :param data: bytes - байтовое значение
        :return: dict - словарь параметров и значений
        """
        new_data = {}
        for key, value in data.items():
            val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[key] = val_decode_str
        return new_data


class DebugApplication(Framework):
    """
    Логирующий класс, для каждого запроса
    выводит информацию (тип запроса и параметры) в консоль.
    """

    def __init__(self, routes_obj, fronts_obj):
        """
        Инициализация логирующего класса
        :param routes_obj: объект маршрутов
        :param fronts_obj: объект фронт контроллера
        """
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


class FakeApplication(Framework):
    """
    Фейковый класс (на все запросы пользователя отвечает: 200 OK, Hello from Fake).
    """

    def __init__(self, routes_obj, fronts_obj):
        """
        Инициализация фейкового класса
        :param routes_obj: объект маршрутов
        :param fronts_obj: объект фронт контроллера
        """
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
