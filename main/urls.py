from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework import routers
router = routers.DefaultRouter()




urlpatterns = [
    path('', views.index, name='index'),
    path('<int:project_id>/', views.project, name='project'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('task/create', views.TaskCreateView.as_view(), name='createtask'),
    path('task/update/<int:pk>', views.TaskUpdateView.as_view(), name='uptatetask'),
    path('project/create', views.ProjectCreateView.as_view(), name='createproject'),
    path('project/update/<int:pk>', views.ProjectUpdateView.as_view(), name='updateproject'),
    path('report/projectbyuser', views.author_project_chart, name='reportproject'),
    path('report/taskbyuser', views.author_task_chart, name='reporttask'),
    path('report/<int:project_id>', views.report, name='report'),
    path('rest/projects/', views.ProjectViewSet.as_view(), name='report'),
    path('rest/users/', views.UserViewSet.as_view(), name='report'),
   
]
