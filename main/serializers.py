from rest_framework import serializers

from . import models


class FullUserSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        tasks = models.Task.objects.filter(author__id=obj.pk)
        return TaskSerializer(tasks, many=True).data

    class Meta:
        model = models.User
        fields = fields = ['last_name', 'first_name', 'patronymic', 'tasks']





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = fields = ['last_name', 'first_name', 'patronymic']




class TaskSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = models.Task
        fields = fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tasks = serializers.SerializerMethodField()

    def get_tasks(self, obj):
        tasks = models.Task.objects.filter(project__id=obj.pk)
        return TaskSerializer(tasks, many=True).data

    class Meta:
        model = models.Project
        fields = fields = '__all__'

