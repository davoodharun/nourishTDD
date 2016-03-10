from selenium import webdriver
import unittest






class NewUserTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		#allow for browser to load (for now)
		self.browser.implicitly_wait(3)
	
	def tearDown(self):
		self.browser.quit()

	def test_can_create_a_storage_and_get_it_later(self):
		self.browser.get('http://localhost:8000')
		# Title and Header should include 'Nourish'
		self.assertIn('Nourish', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').header_text
		self.assertIn('Nourish', header_text)

		#Can has a create group option button
		create_group_button = self.browser.find_elements_by_id('create_group_button')
		self.assertEqual(create_group_button.get_attribute('name'), 'create_group')

		#Once button is clicked, user can see create_group form
		create_group_button.click()
		create_group_form = self.browser.find_element_by_id('create_group_from')
		self.assertEqual(create_group_form.get_attribute('method'), 'POST')

		#Can remove (undo) added items from group

		#Can remove items from group

		#Is updated when item expires or is removed

		#User's group is remembered (persistent storage)
if __name__ == '__main__':
	unittest.main(warnings='ignore')

