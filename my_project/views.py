from datetime import date

from geek_framework.templator import render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer

site = Engine()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
routes = {}


class NotFound404:
    """404 Page Not Found view."""

    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/')
class Index:
    """Index view."""

    def __call__(self, request):
        return '200 OK', render('index.html', date=date.today())


@AppRoute(routes=routes, url='/examples/')
class Examples:
    """Examples view."""

    def __call__(self, request):
        return '200 OK', render('examples.html', date=date.today())


@AppRoute(routes=routes, url='/contacts/')
class Contacts:
    """Contacts view."""

    def __call__(self, request):
        return '200 OK', render('contact.html', date=date.today())


@AppRoute(routes=routes, url='/courses_list/')
class CreateCourse:
    """Create course view."""
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['course_name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('record', name, category)
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)
            return '200 OK', render(
                'courses_list.html',
                objects_list=category.courses,
                name=category.name,
                id=category.id
            )
        else:
            logger.log('Список курсов')
            try:
                self.category_id = int(request['data']['id'])
                category = site.find_category_by_id(
                    int(request['data']['id']))
                return '200 OK', render(
                    'courses_list.html',
                    objects_list=category.courses,
                    name=category.name,
                    id=category.id
                )
            except KeyError:
                return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/category_list/')
class CreateCategory:
    """Create category view."""

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['category_name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render(
                'category_list.html',
                objects_list=site.categories
            )
        else:
            logger.log('Список категорий')
            return '200 OK', render(
                'category_list.html',
                objects_list=site.categories
            )


@AppRoute(routes=routes, url='/copy_course/')
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
            return '200 OK', render(
                'courses_list.html',
                objects_list=site.courses,
                name=new_course.category.name
            )
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/student_list/')
class StudentCreateView(ListView, CreateView):
    """Student list and create view."""
    queryset = site.students
    template_name = 'student_list.html'

    def create_obj(self, data: dict):
        """Create student object."""
        name = data['student_name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add_student/')
class AddStudentByCourseCreateView(CreateView):
    """Add student by course view."""
    template_name = 'add_student.html'

    def get_context_data(self):
        """Get context data method."""
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        """Add student to course method."""
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    """Course API view."""

    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
