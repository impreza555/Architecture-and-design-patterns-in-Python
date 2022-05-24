from datetime import date
from views import Index, Examples, Contacts, Page, CoursesList, \
    CreateCourse, CreateCategory, CategoryList, CopyCourse


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/examples/': Examples(),
    '/contacts/': Contacts(),
    '/page/': Page(),
    '/another_page/': CategoryList(),
}
