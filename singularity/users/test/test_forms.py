from django.test import TestCase
from users.forms import UserUpdateForm

class TestForms(TestCase):

    def test_update_form_valid_data(self):
        """Test for valid update form"""

        form = UserUpdateForm(data={
            'username': 'Praveen', 
            'email': 'Praveen.t@gmail.com'
        })

        self.assertTrue(form.is_valid())

    def test_update_form_valid_data(self):
        """Test for invalid update form"""

        form = UserUpdateForm(data={ })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)