

from .models import LogWork, Project, Task, Membership
from datetime import datetime
from functools import wraps

def calcTimeForTask(tasks, user_id):
    calc = []
    for task in tasks:
        logs = LogWork.objects.filter(task_id=task.id, user_id=user_id)
        sum = 0
        for log in logs:
            sum+=log.logedTime
        calc.append((task, sum))

    return calc


def getMonthStatistics(user_id):
    data = []
    labels = []
                         
    now = datetime.now()
    memberships = Membership.objects.filter(user_id=user_id, status='A').values('project_id')

    user_projects_list = Project.objects.filter(id__in=memberships)

    for project in user_projects_list:
        tasks = Task.objects.filter(project_id=project.id)
        sum=0
        for task in tasks:
            logs = LogWork.objects.filter(task_id=task.id, user_id=user_id)
            for log in logs:
                sum+=log.logedTime
        data.append(sum)
        labels.append(project.name)


    return {
        'data': data,
        'labels':labels
    } 
