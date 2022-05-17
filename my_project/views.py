from geek_framework.templator import render


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
        return '200 OK', render('page.html', date=request.get('date', None))


class AnotherPage:
    """Another page view."""

    def __call__(self, request):
        return '200 OK', render('another_page.html', date=request.get('date', None))
