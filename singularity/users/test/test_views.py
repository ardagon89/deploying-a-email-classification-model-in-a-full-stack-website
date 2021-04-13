from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile

class TestViews(TestCase):

    def setUp(self):
        """Actions to perform before each testcase"""

        self.client = Client()

    def test_register_get(self):
        """Test GET method of register"""
        
        response = self.client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_profile_get(self):
        """Test GET method of profile"""
        
        response = self.client.get(reverse('profile'))

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'users/profile.html')

    def test_classify_get(self):
        """Test GET method of classify"""
        
        response = self.client.get(reverse('classify'))

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'users/classify.html')

    def test_result_get(self):
        """Test GET method of result"""
        
        response = self.client.get(reverse('result'))

        self.assertEquals(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'users/result.html')

    def test_register_post(self):
        """Test POST method of register"""
        
        response = self.client.post(reverse('register'), {
            'username': 'shariq', 
            'email': 'shariq.mellon@gmail.com', 
            'password1': 'shariq.ali#123', 
            'password2': 'shariq.ali#123'
        })

        self.assertEquals(response.status_code, 302)
        self.assertEquals(User.objects.count(), 1)