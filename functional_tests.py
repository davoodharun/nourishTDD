from selenium import webdriver
import unittest






class NewUserTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		#allow for browser to load (for now)
		self.implicitly_wait(3)
	
	def tearDown(self):
		self.browser.quit()

	def test_can_create_a_storage_and_get_it_later(self):
		self.browser.get('http://localhost:8000')
		# Title should be Nourish
		self.assertIn('Nourish', self.browser.title)
		self.fail('incomplete test...')
		#User can login

		#Can create a group

		#Can add items to the group with associated data

		#Can remove (undo) added items from group

		#Can remove items from group

		#Is updated when item expires or is removed

		#User's group is remembered (persistent storage)
if __name__ == '__main__':
	unittest.main(warnings='ignore')

