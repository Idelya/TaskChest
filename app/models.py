from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Project(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Membership(models.Model):
    STATUS_TYPE = (('U','UNKNOWN'), ('U','ACCEPTED'), ('R','REJECTED'))
    status = models.CharField(max_length=1, choices=STATUS_TYPE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    isCreator = models.BooleanField(default=False)

class Table(models.Model):
    name = models.CharField(max_length=30)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Sprint(models.Model):
    num = models.PositiveIntegerField()
    active = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Task(models.Model):
    TASK_TYPE = (('B','BUG'),('F','FEATURE'),('M','MAINTENANCE'), ('S','STORY'))
    name = models.CharField(max_length=30)
    estimate = models.PositiveIntegerField(default=0)
    priority = models.PositiveIntegerField(default=10)
    describe = models.TextField(null=True)
    task_type = models.CharField(max_length=1, choices=TASK_TYPE, default='F')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
    assigned_users = models.ManyToManyField(User, through='Assign')

class Notify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField()
    readed_datetime = models.DateTimeField(null=True)
    describe  = models.TextField(null=True)

    class Meta:
        abstract = True

class Invitation(Notify):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class TasksNotify(Notify):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class Assign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

class LogWork(models.Model):
    logedTime = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateTimeField()
