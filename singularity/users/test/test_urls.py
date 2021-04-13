from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import register, profile, classify, result

class TestUrls(SimpleTestCase):

    def test_register_is_resolved(self):
        """To test if the register path is resolved correctly"""

        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_profile_is_resolved(self):
        """To test if the profile path is resolved correctly"""
        
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)

    def test_classify_is_resolved(self):
        """To test if the classify path is resolved correctly"""
        
        url = reverse('classify')
        self.assertEquals(resolve(url).func, classify)

    def test_result_is_resolved(self):
        """To test if the result path is resolved correctly"""
        
        url = reverse('result')
        self.assertEquals(resolve(url).func, result)