from django.core.urlresolvers import resolve
from django.test import TestCase
from fridges.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from fridges.models import Store, Item

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

# Model Tests
class StoreItemModelTest(TestCase):
    
    def test_save_retrieve_store(self):
        store = Store()
        store.save()

        first_item = Item()
        first_item.text = 'item 1'
        first_item.store = store
        first_item.save()

        second_item = Item()
        second_item.text = 'item 2'
        second_item.store = store
        second_item.save()

        store1 = Store.objects.first()
        self.assertEqual(store1, store)

        items = Item.objects.all()
        self.assertEqual(Item.objects.count(), 2)

        first_saved_item = items[0]
        second_saved_item = items[1]

        self.assertEqual(first_saved_item.text, 'item 1')
        self.assertEqual(second_saved_item.text, 'item 2')
        self.assertEqual(first_saved_item.store, store)
        self.assertEqual(second_saved_item.store, store)


class StoreViewTest(TestCase):

    def uses_store_template(self):
        response = self.client.get('/stores/%d/' % (store.id))
        self.assertTemplateUsed(response, 'store.html')

    def test_displays_all_items_for_specific_store(self):
        store1 = Store.objects.create()
        Item.objects.create(text='item 1', store=store1)
        Item.objects.create(text='item 2', store=store1)
        store2 = Store.objects.create()
        Item.objects.create(text='item 3', store=store2)
        Item.objects.create(text='item 4', store=store2)

        response = self.client.get('/stores/%d/' % (store1.id))

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'item 3')
        self.assertNotContains(response, 'item 4')

class NewStoreTest(TestCase):

    def test_can_save_post_request(self):
        self.client.post(
            '/stores/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Store.objects.count(), 1)
        new_item = Store.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        

    def test_redirects_after_post_request(self):
        response = self.client.post(
            '/stores/new',
            data={'item_text': 'A new list item'}
        )

        new_store = Store.objects.first()
        self.assertRedirects(response, '/stores/%d/' % (new_store.id))

class NewItemTest(TestCase):

    def test_can_save_POST_item_to_existing_list(self):
        store2 = Store.objects.create()
        store1 = Store.objects.create()

        self.client.post(
            '/stores/%d/add_item' % (store1.id),
            data={'item_text': 'item for list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'item for list')
        self.assertEqual(item.list, store1)

        response = self.client.post(
            '/stores/%d/add_item' % (store1.id),
            data={'item_text': 'item for list'}
        )

        self.assertRedirects(response, '/stores/%d/' % (store1.id))

    def test_correct_store_given_to_template(self):
        store2 = Store.objects.create()
        store1 = Store.objects.create()
        response = self.client.get('stores/%d/' % (store1.id))
        self.assertEqual(response.context['lists'], store1)