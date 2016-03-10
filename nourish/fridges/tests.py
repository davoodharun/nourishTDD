from django.test import TestCase

class FakeTest(TestCase):
    def test_fake(self):
        self.assertEqual(1, 3)
