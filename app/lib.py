

from .models import LogWork

def calcTimeForTask(tasks):
    calc = []
    for task in tasks:
        logs = LogWork.objects.filter(task_id=task.id)
        sum = 0
        for log in logs:
            sum+=log.logedTime
        calc.append((task, sum))

    return calc