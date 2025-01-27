from .models import Resource, Kernel
from rest_framework import serializers
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class KernelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kernel
        fields = '__all__'
