class GetRequests:
    """
    Класс обработки Get запросов
    """

    def __init__(self, environ):
        """
        Инициализация класса.
        :param environ: dict - словарь данных от сервера
        """
        self.environ = environ

    def get_request_params(self):
        """
        Получение параметров запроса.
        :return: dict - словарь параметров и значений запроса
        """
        query_string = self.environ['QUERY_STRING']
        request_params = parse_input_data(query_string)
        return request_params


class PostRequests:
    """
    Класс обработки Post запросов
    """

    def __init__(self, environ):
        """
        Инициализация класса.
        :param environ: dict - словарь данных от сервера
        """
        self.environ = environ

    def post_request_params(self):
        """
        Получение параметров запроса.
        :return: dict - словарь параметров и значений запроса
        """
        result = {}
        content_length_data = self.environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        print(content_length)
        data = self.environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        if data:
            data_str = data.decode(encoding='utf-8')
            print(f'строка после декодирования - {data_str}')
            result = parse_input_data(data_str)
        return result


def parse_input_data(data: str):
    """
    Парсинг параметров запроса.
    :param data: str - строка запроса
    :return: dict - словарь параметров и значений запроса
    """
    result = {}
    if data:
        params = data.split('&')
        for item in params:
            key, value = item.split('=')
            result[key] = value
    return result
