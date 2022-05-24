from geek_framework.templator import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class NotFound404:
    """
    404 Page Not Found view
    """

    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Index:
    """Index view."""

    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))


class Examples:
    """Examples view."""

    def __call__(self, request):
        return '200 OK', render('examples.html', date=request.get('date', None))


class Contacts:
    """Contacts view."""

    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))


class Page:
    """Page view."""

    def __call__(self, request):
        return '200 OK', render('page.html', date=request.get('date', None), objects_list=site.categories)


# class AnotherPage:
#     """Another page view."""
#
#     def __call__(self, request):
#         return '200 OK', render('another_page.html', date=request.get('date', None))


# контроллер - список курсов
class CoursesList:
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('another_page.html',
                                    objects_list=category.courses,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


class CreateCourse:
    """Create course view."""
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('another_page.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


class CreateCategory:
    """Create category view."""

    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('page.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('page.html',
                                    categories=categories)


class CategoryList:
    """Category list view."""

    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('page.html',
                                objects_list=site.categories)


class CopyCourse:
    """Copy course view."""

    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('another_page.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
