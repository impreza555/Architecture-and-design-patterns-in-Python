from datetime import date
from views import Index, Examples, Contacts, CreateCategory, CopyCourse, CreateCourse


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/examples/': Examples(),
    '/contacts/': Contacts(),
    '/category_list/': CreateCategory(),
    '/courses_list/': CreateCourse(),
    '/copy_course/': CopyCourse()
}
