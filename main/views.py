from django.shortcuts import render, redirect
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate, login,logout 
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from rest_framework import permissions, viewsets

from . import models 
from . import forms 
from . import serializers 

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
def index(request):
    reports = models.Report.objects.all()
    projects = models.Project.objects.all()
    return render(request, 'main/index.html', {'projects':projects, 'reports' : reports})


def login_view(request):
    if request.method == "POST":
        username = request.POST["login"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        return render(request, 'main/login.html', {'error' : 'Пользователь не найден'})
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect(index)


def project(request, project_id):
    project = models.Project.objects.get(id=project_id)
    tasks = models.Task.objects.filter(project=project)
    wip_tasks = tasks.filter(status='vip')
    done_tasks = tasks.filter(status='done')
    reup_tasks = tasks.filter(status='JR')
    all_count = len(tasks)
    done_count = len(done_tasks)
    reup_count = len(reup_tasks)
    return render(request, 'main/project.html', {'project':project, 'wip_tasks': wip_tasks, 'done_tasks' : done_tasks, 'reup_tasks' : reup_tasks, 'all_count' : all_count, 'done_count':done_count, 'reup_count': reup_count})




def report(request, project_id):
    report = models.Report.objects.filter(project__id=project_id)
    project = models.Project.objects.get(id=project_id)
    if not report:
        report = models.Report.objects.create(project=project)
        report.save()

    tasks = models.Task.objects.filter(project__id=project_id)
    dates = []
    for task in tasks:
        date = task.create_at
        dates.append(date)
    print(dates)
    counts = []
    for date in dates:
        count = models.Task.objects.filter(create_at__lte=date).count()
        counts.append(count)
    counts = sorted(counts)
    label = 'Количество задач по дням'
    return render(request, 'main/chart.html', {'dates':dates, 'counts':counts, 'label':label})


def author_project_chart(request):
    users = models.User.objects.all()
    users_data = []
    counts = []
    for user in users:
        users_data.append(user)
        count = models.Project.objects.filter(author=user).count()
        counts.append(count)

    label = 'Количество проектов у сотрудников'
    return render(request, 'main/chart.html', {'dates':users_data, 'counts':counts, 'label':label})


def author_task_chart(request):
    users = models.User.objects.all()
    users_data = []
    counts = []
    for user in users:
        users_data.append(user)
        count = models.Task.objects.filter(author=user).count()
        counts.append(count)

    label = 'Количество задач у сотрудников'
    return render(request, 'main/chart.html', {'dates':users_data, 'counts':counts, 'label':label})



class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    form_class = forms.TaskForm
    template_name = 'main/task.html'
    success_url = reverse_lazy(index)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'main/task.html'
    success_url = reverse_lazy(index)

    def get_success_url(self):
           pk = self.kwargs["pk"]
           task = models.Task.objects.get(id=pk)
           return reverse("project", kwargs={"project_id": task.project.id})

class ProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    form_class = forms.ProjectForm
    template_name = 'main/task.html'
    success_url = reverse_lazy(index)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'main/task.html'


    def get_success_url(self):
           pk = self.kwargs["pk"]
           return reverse("project", kwargs={"project_id": pk})


    



class UserViewSet(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        data = models.User.objects.all()
        serializer = serializers.FullUserSerializer(data, many=True)

        return Response(serializer.data)


class ProjectViewSet(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        data = models.Project.objects.all()
        serializer = serializers.ProjectSerializer(data, many=True)

        return Response(serializer.data)