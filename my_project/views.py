from datetime import date

from geek_framework.templator import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class NotFound404:
    """404 Page Not Found view."""

    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Index:
    """Index view."""

    def __call__(self, request):
        return '200 OK', render('index.html', date=date.today())


class Examples:
    """Examples view."""

    def __call__(self, request):
        return '200 OK', render('examples.html', date=date.today())


class Contacts:
    """Contacts view."""

    def __call__(self, request):
        return '200 OK', render('contact.html', date=date.today())


class CreateCourse:
    """Create course view."""
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['course_name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('courses_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        else:
            logger.log('Список курсов')
            try:
                self.category_id = int(request['data']['id'])
                category = site.find_category_by_id(
                    int(request['data']['id']))
                return '200 OK', render('courses_list.html',
                                        objects_list=category.courses,
                                        name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No courses have been added yet'


class CreateCategory:
    """Create category view."""

    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['category_name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('category_list.html', objects_list=site.categories)
        else:
            logger.log('Список категорий')
            return '200 OK', render('category_list.html',
                                    objects_list=site.categories)


class CopyCourse:
    """Copy course view."""

    def __call__(self, request):
        request_params = request['data']

        try:
            name = request_params['name']

            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('courses_list.html',
                                    objects_list=site.courses,
                                    name=new_course.category.name)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
