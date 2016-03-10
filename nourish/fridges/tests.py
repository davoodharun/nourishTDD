from django.core.urlresolvers import resolve
from django.test import TestCase
from fridges.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

class HomePageTest(TestCase):
    def test_rool_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        #request object
        request = HttpRequest()
        #response object
        response = home_page(request)
        expected_html = render_to_string('home.html')
        #porting assertion to bytes
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_form_can_save_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new storage item'

        response = home_page(request)

        self.assertIn('A new storage item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_group_text': 'A new storage item'}
        )
        self.assertEqual(response.content.decode(), expected_html   )