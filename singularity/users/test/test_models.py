from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile

class TestModels(TestCase):

    def setUp(self):
        """Actions to perform before each testcase"""

        self.client = Client()

        self.user1 = User.objects.create(
            username = 'shariq', 
            email = 'shariq.mellon@gmail.com'
        )

    def test_user_create_count(self):
        """Test the record count after create method of User"""
        
        self.assertEquals(User.objects.count(), 1)

    def test_user_create_value(self):
        """Test the username value after create method of User"""
        
        self.assertEquals(User.objects.first().username, 'shariq')

    def test_profile_create_count(self):
        """Test the record count after create method of Profile"""
        
        self.assertEquals(Profile.objects.count(), 1)

    def test_profile_create_value(self):
        """Test the record value after create method of Profile"""
        
        self.assertEquals(Profile.objects.first().first_name, '')

    def test_profile_update_values(self):
        """Test the record value after create method of Profile"""

        profile = Profile.objects.first()
        profile.first_name = 'Shariq'
        profile.last_name = 'Ali'
        profile.save()
        
        self.assertEquals(Profile.objects.first().first_name, 'Shariq')
        self.assertEquals(Profile.objects.first().last_name, 'Ali')