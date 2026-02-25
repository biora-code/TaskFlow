from rest_framework import serializers
from .models import Task


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'due_date', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user',)