from . import models 
from django.forms import ModelForm



class ProjectForm(ModelForm):
    class Meta:
        model = models.Project
        fields = '__all__'

class TaskForm(ModelForm):
    class Meta:
        model = models.Task
        fields = '__all__'