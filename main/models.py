from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
	last_name = models.CharField('Фамилия', max_length=30, blank=True)
	first_name = models.CharField('Имя', max_length=30, blank=True)
	patronymic = models.CharField('Отчество', max_length=30, blank=True)

	def __str__(self):
		return f'{self.last_name} {self.first_name} {self.patronymic}.'
    




status_set = [
    ("vip", "В работе"),
    ("done", "Завершен(а)"),
    ("JR", "Требуется исправления"),
    
]

class Project(models.Model):
	name = models.CharField('Название проекта', max_length=100)
	status = models.CharField(max_length=4, choices=status_set,verbose_name='Статус')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
	

	def __str__(self):
		return self.name


	class Meta:
		verbose_name = 'Проект'
		verbose_name_plural = 'Проекты'



class Task(models.Model):
	name = models.CharField('Название задачи', max_length=100)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
	status = models.CharField(max_length=4, choices=status_set,verbose_name='Статус')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
	create_at = models.DateField(verbose_name='Дата создания')
	deadline = models.DateField(verbose_name='Дедлайн')
	description = models.TextField('Описанние')
	attachment = models.FileField(upload_to ='uploads/', verbose_name='Файл', blank=True, null=True)

	def __str__(self):
		return self.name


	class Meta:
		verbose_name = 'Задача'
		verbose_name_plural = 'Задачи'

class Report(models.Model):
	create_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
	project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')


	def __str__(self):
		return f'{self.project.name} {self.create_at}'


	class Meta:
		verbose_name = 'Задача'
		verbose_name_plural = 'Задачи'