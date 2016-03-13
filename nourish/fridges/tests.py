from django.core.urlresolvers import resolve
from django.test import TestCase
from fridges.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from fridges.models import Store

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
        request.POST['store_text'] = 'A new store item'

        response = home_page(request)

        self.assertEqual(Store.objects.count(), 1)
        self.assertEqual(Store.objects.all()[0].text, 'A new store item')

    def test_redirects_after_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['store_text'] = 'A new store item'

        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/stores/the-only-store/')

    def test_home_page_from_saves_post_requests_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Store.objects.count(), 0)

    def test_shows_all_stores(self):
        Store.objects.create(text='store1')
        Store.objects.create(text='store2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('store1', response.content.decode())
        self.assertIn('store2', response.content.decode())

class StoreModelTest(TestCase):
    
    def test_save_retrieve_store(self):
        first_store = Store()
        first_store.text = 'Store item 1'
        first_store.save()

        second_store = Store()
        second_store.text = 'Store item 2'
        second_store.save()
        
        saved_items = Store.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0].text, 'Store item 1')
        self.assertEqual(saved_items[1].text, 'Store item 2')

class StoreViewTest(TestCase):

    def uses_store_template(self):
        response = self.client.get('/stores/the-only-store/')
        self.assertTemplateUsed(response, 'store.html')

    def test_displays_all_items(self):
        Store.objects.create(text='item 1')
        Store.objects.create(text='item 2')

        response = self.client.get('/stores/the-only-store/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
