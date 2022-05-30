from time import time


class AppRoute:
    """
    Класс - структурный паттерн декоратор.
    Сопоставляет маршруты и урлы.
    """

    def __init__(self, routes, url):
        """
        Инициализация декоратора
        :param routes: Словарь маршрутов
        :param url: Словарь урлов
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    """
    Класс - структурный паттерн декоратор.
    Реализует декоратор для отладки классов.
    """

    def __init__(self, name):
        """
        Инициализация декоратора.
        :param name: имя класса
        """
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            """
            Оборачивает каждый метод декорируемого класса в timeit.
            :param method: метод декорируемого класса
            :return: None
            """

            def timed(*args, **kw):
                """
                Метод замеряет время выполнения метода декорируемого класса.
                :param args:
                :param kw:
                :return: function
                """
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts
                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
