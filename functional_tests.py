from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('Nourish', header_text)


		#Once button is clicked, user can see create_group form with input for group name and submit button
		create_group_form = self.browser.find_element_by_id('create_group_from')
		self.assertEqual(create_group_form.get_attribute('method'), 'post')
		input_tags = self.browser.find_elements_by_tag_name('input')
		self.assertTrue(
			any(input_tag.get_attribute('name') == 'item_text' for input_tag in input_tags), "could not find input bodx with name group_name"
		)
		#User can add groups; enter group name in input and see it in table
		input_box = self.browser.find_element_by_id('group_field')
		self.assertEqual(input_box.get_attribute('placeholder'), 'Enter group name')
	
		input_box.send_keys('Fridge')
		input_box.send_keys(Keys.ENTER)

		table = self.browser.find_element_by_id('groups_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('Fridge', [row.text for row in rows])
		#Can remove (undo) added items from group

		#Can remove items from group

		#Is updated when item expires or is removed

		#User's group is remembered (persistent storage)
if __name__ == '__main__':
	unittest.main(warnings='ignore')

