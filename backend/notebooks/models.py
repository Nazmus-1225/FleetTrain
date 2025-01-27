from django.db import models
from accounts.models import User
# Create your models here.
class Notebook(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default='')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    file_location = models.CharField(max_length=255)
    type = models.CharField(max_length=50)

class Dataset(models.Model):
    id = models.AutoField(primary_key=True)
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)

class Cell(models.Model):
    id = models.AutoField(primary_key=True)
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    contents = models.TextField()