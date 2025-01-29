from .models import Notebook, Cell, NotebookLocations
from rest_framework import serializers
class NotebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notebook
        fields = '__all__'

class NotebookLocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotebookLocations   
        fields = '__all__'

class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = '__all__'
