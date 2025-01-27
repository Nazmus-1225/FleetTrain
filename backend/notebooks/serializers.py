from .models import Notebook
from rest_framework import serializers
class NotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notebook
        fields = '__all__'
