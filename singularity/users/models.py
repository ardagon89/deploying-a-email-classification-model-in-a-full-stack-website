from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    first_name = models.CharField( max_length=100, editable=True, blank=True)
    middle_name = models.CharField( max_length=100, editable=True, blank=True)
    last_name = models.CharField( max_length=100, editable=True, blank=True)
    phone_number = models.CharField( max_length=100, editable=True, blank=True)
    mail_address = models.CharField( max_length=100, editable=True, blank=True)
    occupation = models.CharField( max_length=100, editable=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user.username} Profile'