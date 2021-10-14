from django.db import models
from django.contrib.auth.models import User, PermissionsMixin
# Create your models here.

class User(User,PermissionsMixin):
    
    def __str__(self):
        return self.username
        
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False