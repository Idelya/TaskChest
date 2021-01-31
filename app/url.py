from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('statistics/', views.statistics, name='statistics'),
    path('notifications/', views.notifications, name='notifications'),
    path('projects/', views.projects, name='projects'),
    path('tasks/', views.tasks, name='tasks'),
    path('signup/', views.signup, name='signup'),
    path('newproject/', views.newproject, name='newproject'),
    path('invitation-accept/', views.invitationAccept, name='invitationAccept'),
    path('invitation-discard/', views.invitationDiscard, name='invitationDiscard'),
    path('project/<id>', views.projectManage, name='projectManage'),
    path('taskcreate/<id>', views.taskCreate, name='taskCreate'),
    path('taskview/<id>', views.taskView, name='taskView'),
    path('taskedit/<id>', views.taskEdit, name='taskEdit'),
    path('logtime/<id>',views.logTime, name='logTime'),
]