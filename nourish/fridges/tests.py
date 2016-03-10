from django.core.urlresolvers import resolve
from django.test import TestCase
from fridges.views import home_page
from django.http import HttpRequest

class HomePageTest(TestCase):
    def test_rool_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        #request object
        request = HttpRequest()
        #response object
        response = home_page(request)
        #porting assertion to bytes
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Welcome to Nourish!</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))