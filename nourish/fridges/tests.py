from django.core.urlresolvers import resolve
from django.test import TestCase
from fridges.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from fridges.models import Fridge, Item

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
        request.POST['fridge_text'] = 'A new fridge item'

        response = home_page(request)

        self.assertEqual(Fridge.objects.count(), 1)
        self.assertEqual(Fridge.objects.all()[0].text, 'A new fridge item')

    def test_redirects_after_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['fridge_text'] = 'A new fridge'

        response = home_page(request)
        self.assertEqual(response.status_code, 302)
        fridge = Fridge.objects.last()
        self.assertEqual(response['location'], '/fridges/%d/' % (fridge.id))

    def test_home_page_from_saves_post_requests_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Fridge.objects.count(), 0)

    def test_shows_all_fridges(self):
        Fridge.objects.create(text='fridge1')
        Fridge.objects.create(text='fridge2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('fridge1', response.content.decode())
        self.assertIn('fridge2', response.content.decode())

# Model Tests
class FridgeItemModelTest(TestCase):
    
    def test_save_retrieve_fridge(self):
        fridge = Fridge()
        fridge.save()

        first_item = Item()
        first_item.text = 'item 1'
        first_item.fridge = fridge
        first_item.save()

        second_item = Item()
        second_item.text = 'item 2'
        second_item.fridge = fridge
        second_item.save()

        fridge1 = Fridge.objects.first()
        self.assertEqual(fridge1, fridge)

        items = Item.objects.all()
        self.assertEqual(Item.objects.count(), 2)

        first_saved_item = items[0]
        second_saved_item = items[1]

        self.assertEqual(first_saved_item.text, 'item 1')
        self.assertEqual(second_saved_item.text, 'item 2')
        self.assertEqual(first_saved_item.fridge, fridge)
        self.assertEqual(second_saved_item.fridge, fridge)


class FridgeViewTest(TestCase):

    def uses_fridge_template(self):
        response = self.client.get('/fridges/%d/' % (fridge.id))
        self.assertTemplateUsed(response, 'fridge.html')

    def test_displays_all_items_for_specific_fridge(self):
        fridge1 = Fridge.objects.create()
        Item.objects.create(text='item 1', fridge=fridge1)
        Item.objects.create(text='item 2', fridge=fridge1)
        fridge2 = Fridge.objects.create()
        Item.objects.create(text='item 3', fridge=fridge2)
        Item.objects.create(text='item 4', fridge=fridge2)

        response = self.client.get('/fridges/%d/' % (fridge1.id))

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'item 3')
        self.assertNotContains(response, 'item 4')

class NewFridgeTest(TestCase):

    def test_can_save_post_request(self):
        self.client.post(
            '/fridges/new',
            data={'fridge_text': 'A new fridge'}
        )
        self.assertEqual(Fridge.objects.count(), 1)
        new_fridge = Fridge.objects.first()
        self.assertEqual(new_fridge.text, 'A new fridge')
        

    def test_redirects_after_post_request(self):
        response = self.client.post(
            '/fridges/new',
            data={'fridge_text': 'A new fridge'}
        )

        new_fridge = Fridge.objects.first()
        self.assertRedirects(response, '/fridges/%d/' % (new_fridge.id))

class NewItemTest(TestCase):

    def test_can_save_POST_item_to_existing_list(self):
        fridge2 = Fridge.objects.create()
        fridge1 = Fridge.objects.create()

        self.client.post(
            '/fridges/%d/add_item' % (fridge1.id),
            data={'item_text': 'item for list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.first()
        self.assertEqual(item.text, 'item for list')
        self.assertEqual(item.fridge, fridge1)

        response = self.client.post(
            '/fridges/%d/add_item' % (fridge1.id),
            data={'item_text': 'item for list'}
        )

        self.assertRedirects(response, '/fridges/%d/' % (fridge1.id))

    def test_correct_fridge_given_to_template(self):
        fridge2 = Fridge.objects.create()
        fridge1 = Fridge.objects.create()
        response = self.client.get('fridges/%d/' % (fridge1.id))
        self.assertEqual(response.context['fridge'].id, fridge1.id)