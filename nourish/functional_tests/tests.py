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
	
		input_box.send_keys('Fridge_user1')

		#when Enter is hit, user is taken to a new url where the Fridge list exists 
		input_box.send_keys(Keys.ENTER)
		user1_store_url = self.browser.current_url
		self.assertRegex(user1_store_url, '/stores/.+')
		self.check_for_row_in_list_table('Fridge_user1')

		self.browser.quit()
		self.browser = Firefox()

		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Fridge_user1', page_text)

		input_box = self.browser.find_element_by_id('group_field')
		self.assertEqual(input_box.get_attribute('placeholder'), 'Enter group name')
		input_box.send_keys('Fridge_user2')

		#when Enter is hit, user is taken to a new url where the Fridge list exists 
		input_box.send_keys(Keys.ENTER)

		user2_store_url = self.browser.current_url
		self.assertRegex(user1_store_url, '/stores/.+')
		self.assertNotEqual(user2_store_url, user1_store_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Fridge_user1', page_text)
		self.assertIn('Fridge_user2', page_text)
if __name__ == '__main__':
	unittest.main(warnings='ignore')

