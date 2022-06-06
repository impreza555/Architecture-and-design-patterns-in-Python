from threading import local


class UnitOfWork:
    """Класс единица работы - архитектурный системный паттерн UnitOfWork."""
    current = local()

    def __init__(self):
        """Инициализация класса UnitOfWork."""
        self.MapperRegistry = None
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        """Установка реестра мапперов для текущего подключения к БД."""
        self.MapperRegistry = MapperRegistry

    def register_new(self, obj):
        """
        Метод регистрации объектов для внесения в БД.
        :param obj: Объект для регистрации.
        :return: None
        """
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        """
        Метод регистрации объектов в БД для изменения.
        :param obj: Объект для регистрации.
        :return: None
        """
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        """
        Метод регистрации объектов для удаления из БД.
        :param obj: Объект для регистрации.
        :return: None
        """
        self.removed_objects.append(obj)

    def commit(self):
        """Метод совершения коммита в БД."""
        self.insert_new()
        self.update_dirty()
        self.delete_removed()
        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()

    def insert_new(self):
        """Метод внесения новых объектов в БД."""
        print(self.new_objects)
        for obj in self.new_objects:
            print(f"Вывожу {self.MapperRegistry}")
            self.MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        """Метод обновления объектов в БД."""
        for obj in self.dirty_objects:
            self.MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        """Метод удаления объектов из БД."""
        for obj in self.removed_objects:
            self.MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        """Метод создания в потоке нового экземпляра класса UnitOfWork."""
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        """Метод установки экземпляра класса UnitOfWork текущим."""
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        """Метод получения текущего экземпляра класса UnitOfWork."""
        return cls.current.unit_of_work


class DomainObject:
    """
    Класс супертипа предметной области, позволяющий объекту модели
    предметной области регистрироваться в текущей единице работы.
    """

    def mark_new(self):
        """Метод помечающий объект в текущей единице работы как новый."""
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        """Метод помечающий объект в текущей единице работы как измененный."""
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        """Метод помечающий объект в текущей единице работы как удаленный."""
        UnitOfWork.get_current().register_removed(self)
