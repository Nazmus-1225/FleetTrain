from django.db import models
from notebooks.models import Notebook
# Create your models here.
class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=100,default='')
    username = models.CharField(max_length=100,default='')
    password = models.CharField(max_length=100,default='')
    ip_address = models.GenericIPAddressField()
    max_kernels = models.PositiveIntegerField()
    used = models.PositiveIntegerField(default=0)
    available = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.available = self.max_kernels - self.used
        super(Resource, self).save(*args, **kwargs)


class Kernel(models.Model):
    id = models.AutoField(primary_key=True)
    kernel_name = models.CharField(max_length=100)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    type = models.CharField(max_length=50,default='central')