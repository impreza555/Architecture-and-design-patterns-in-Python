from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect
from patterns.behavioral_patterns import FileWriter, Subject
from patterns.architectural_patterns import DomainObject

connection = connect('my_project.db')


class User:
    """Абстрактный класс пользователя."""

    def __init__(self, name):
        """Инициализация пользователя."""
        self.name = name


class Teacher(User):
    """Класс пользователя - преподавателя."""
    pass


class Student(User, DomainObject):
    """Класс пользователя - студента."""

    def __init__(self, name):
        """Инициализация пользователя студента."""
        self.courses = []
        super().__init__(name)


class UserFactory:
    """Фабрика пользователей - порождающий паттерн Абстрактная фабрика."""
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name):
        """
        Создание пользователя.
        :param type_:
        :return: cls - Класс нового пользователя.
        """
        return cls.types[type_](name)


class CoursePrototype:
    """Прототип курсов обучения - порождающий паттерн Прототип."""

    def clone(self):
        """
        Метод клонирование объекта курса.
        :return: cls - Класс курса.
        """
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    """Класс - курс обучения."""

    def __init__(self, name, category):
        """
        Конструктор курса.
        :param name: название курса
        :param category: категория курса
        """
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        """Метод получения объекта студента."""
        return self.students[item]

    def add_student(self, student: Student):
        """Метод добавления студента на курс."""
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class InteractiveCourse(Course):
    """Интерактивный курс обучения."""
    pass


class RecordCourse(Course):
    """Курс обучения в записи."""
    pass


class CourseFactory:
    """Фабрика курсов - порождающий паттерн Абстрактная фабрика."""
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        """
        Создание курса.
        :param type_: тип курса
        :param name: название курса
        :param category: категория курса
        :return: cls - Класс нового курса.
        """
        return cls.types[type_](name, category)


class Category:
    """ Класс - категория курсов."""
    auto_id = 0

    def __init__(self, name, category):
        """
        Конструктор категории.
        :param name: название
        :param category: категория
        """
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        """
        Метод подсчёта количества курсов в категории.
        :return: int - количество курсов
        """
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Engine:
    """Движок фреймворка."""

    def __init__(self):
        """
        Конструктор класса движка.
        """
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        """
        Метод создания пользователя.
        :param type_: тип пользователя
        :param name: имя пользователя
        :return: cls - Класс нового пользователя.
        """
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        """
        Метод создания категории.
        :param name: название категории
        :param category: категория
        :return: cls - Класс новой категории.
        """
        return Category(name, category)

    def find_category_by_id(self, id):
        """
        Метод поиска категории по id.
        :param id: int - id категории
        :return: объект категории
        """
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        """
        Метод создания курса.
        :param name: название курса
        :param type_: тип курса
        :param category: категория
        :return: cls - Класс нового курса.
        """
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        """
        Метод поиска курса по названию.
        :param name: название курса.
        :return: объект курса.
        """
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        """
        Метод получения объекта студента по имени.
        :param name: str - имя студента
        :return: объект студента
        """
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        """
        Метод декодирования значения.
        :param val: значение
        :return: декодированное значение
        """
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):
    """Класс порождающий паттерн Singleton."""

    def __init__(cls, name, bases, attrs, **kwargs):
        """
        Конструктор класса.
        :param name:
        :param bases:
        :param attrs:
        :param kwargs:
        """
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        """
        Метод вызова класса.
        :param args:
        :param kwargs:
        :return: cls - объект класса
        """
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    """Класс логгера."""

    def __init__(self, name, writer=FileWriter()):
        """
        Конструктор класса.
        :param name: имя логгера
        """
        self.name = name
        self.writer = writer

    def log(self, text):
        """
        Метод логгирования.
        :param text: str - текст лога
        :return: None
        """
        text = f'log---> {text}'
        self.writer.write(text)


class StudentMapper:
    """Маппер модели студент."""

    def __init__(self, connection):
        """
        Инициализация маппера.
        :param connection: объект подключения к базе данных
        """
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'student'

    def all(self):
        """
        Метод запроса всех данных из таблицы.
        :return: list - список объектов
        """
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        """
        Метод получения объекта из таблицы по id.
        :param id: int - id объекта
        :return: объект студента
        """
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        """
        Метод вставки объекта в таблицу.
        :param obj: объект студента
        """
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        """
        Метод обновления объекта в таблице.
        :param obj: объект студента
        """
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        """
        Метод удаления объекта из таблицы.
        :param obj: объект студента
        """
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    """Реестр мапперов - системный паттерн Data Mapper."""
    mappers = {
        'student': StudentMapper,
    }

    @staticmethod
    def get_mapper(obj):
        """
        Метод получения маппера по объекту.
        :param obj: объект
        :return: объект маппера
        """
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        """
        Метод получения текущего маппера по имени.
        :param name: имя маппера
        :return: объект текущего маппера
        """
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    """Класс - исключение при выполнении коммита базы данных."""

    def __init__(self, message):
        """Метод инициализации исключения."""
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    """Класс - исключение при выполнении обновления базы данных."""

    def __init__(self, message):
        """Метод инициализации исключения."""
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    """Класс - исключение при выполнении удаления базы данных."""

    def __init__(self, message):
        """Метод инициализации исключения."""
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    """Класс - исключение при не найденном объекте в базе данных."""

    def __init__(self, message):
        """Метод инициализации исключения."""
        super().__init__(f'Record not found: {message}')
