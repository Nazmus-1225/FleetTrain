from django.db import models
from django.contrib.auth.models import User

class Notebook(models.Model):
    # Remove the erroneous str = part
    title = models.CharField(max_length=200)  # Fixed: removed str =
    content = models.JSONField(default=dict)  # Added default=dict
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']