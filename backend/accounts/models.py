from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, choices=(('user', 'User'), ('admin', 'Admin')), default='user')

    def save(self, *args, **kwargs):
        if not self.id:  # Hash password on creation
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
