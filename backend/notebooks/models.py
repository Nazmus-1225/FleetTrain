from django.db import models
from accounts.models import User
# Create your models here.
class Notebook(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,default='')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50)
    num_of_nodes = models.IntegerField(default=1)

class NotebookLocations(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    location = models.CharField(max_length=500,default='')