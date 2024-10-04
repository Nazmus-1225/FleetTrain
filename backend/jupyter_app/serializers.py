from django_restframework import serializers
from .models import Notebook
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class NotebookCellSerializer(serializers.Serializer):
    id = serializers.CharField()
    type = serializers.ChoiceField(choices=['code', 'markdown'])
    content = serializers.CharField()
    outputs = serializers.JSONField(default=list)

class NotebookSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    cells = NotebookCellSerializer(many=True)

    class Meta:
        model = Notebook
        fields = ['id', 'title', 'content', 'cells', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        cells_data = validated_data.pop('cells', [])
        # Get the current user from the context
        user = self.context['request'].user
        notebook = Notebook.objects.create(owner=user, **validated_data)
        
        # Store cells in the JSONField
        notebook.content = {'cells': cells_data}
        notebook.save()
        
        return notebook

    def update(self, instance, validated_data):
        cells_data = validated_data.pop('cells', [])
        
        # Update the notebook fields
        instance.title = validated_data.get('title', instance.title)
        
        # Update the cells in the JSONField
        instance.content = {'cells': cells_data}
        instance.save()
        
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Move cells from content to top level
        representation['cells'] = instance.content.get('cells', [])
        return representation