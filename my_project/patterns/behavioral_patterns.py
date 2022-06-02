from jsonpickle import dumps, loads
from geek_framework.templator import render


class Observer:
    """Класс наблюдатель - поведенческий паттерн - наблюдатель."""

    def update(self, subject):
        pass


class Subject:
    """Класс объекта наблюдения."""

    def __init__(self):
        """Конструктор объекта наблюдения."""
        self.observers = []

    def notify(self):
        """Метод оповещения."""
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):
    """Класс оповещения по SMS."""

    def update(self, subject):
        """Метод оповещения по SMS."""
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):
    """Класс оповещения по EMAIL."""

    def update(self, subject):
        """Метод оповещения по EMAIL."""
        print('EMAIL->', 'к нам присоединился', subject.students[-1].name)


class BaseSerializer:
    """Базовый класс сериализатора - паттерн хранитель."""

    def __init__(self, obj):
        """Конструктор базового класса сериализатора."""
        self.obj = obj

    def save(self):
        """Метод сериализации объекта."""
        return dumps(self.obj)

    @staticmethod
    def load(data):
        """Метод десериализации объекта."""
        return loads(data)


class TemplateView:
    """Класс представления поведенческий паттерн - Шаблонный метод."""
    template_name = 'template.html'

    def get_context_data(self):
        """Метод получения контекста представления."""
        return {}

    def get_template(self):
        """Метод получения шаблона."""
        return self.template_name

    def render_template_with_context(self):
        """Метод рендеринга шаблона с контекстом."""
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    """Класс представления контекста в шаблоне."""
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        """Метод получения контекста представления."""
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        """Метод получения имени объекта контекста."""
        return self.context_object_name

    def get_context_data(self):
        """Метод получения словаря контекста."""
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    """Класс представления создания объекта."""
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        """Метод получения данных из запроса."""
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context()
        else:
            return super().__call__(request)


# поведенческий паттерн - Стратегия
class ConsoleWriter:
    """Класс описания поведенческого паттерна - Стратегия - Консольный вывод."""

    def write(self, text):
        """Метод вывода в консоль."""
        print(text)


class FileWriter:
    """Класс описания поведенческого паттерна - Стратегия - Файловый вывод."""

    def __init__(self):
        """Конструктор класса."""
        self.file_name = 'log.txt'

    def write(self, text):
        """Метод вывода в файл."""
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
