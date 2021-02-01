from __future__ import annotations
from abc import ABC, abstractmethod
from .models import Notify, Invitation, TasksNotify, Task, Project
from datetime import datetime

class NotyficationsContext():

    def __init__(self, strategy: Strategy) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    
    def createNew(self, from_user, to_user, id, describe):
        self._strategy.createNotify(from_user, to_user, id, describe)

    def setAllAsReaded():
        pass


class Strategy(ABC):
    @abstractmethod
    def createNotify(self, from_user, to_user, id, describe):
        pass

    @abstractmethod
    def setAsReaded(self, id):
        pass


class NotifyTaskStrategy(Strategy):
    def createNotify(self, from_user, to_user, id, describe):
        task = Task.objects.get(pk=id)
        notify = TasksNotify(user=to_user,  created_datetime=datetime.now(), describe=describe, task=task)
        notify.save()
    
    def setAsReaded(self, id):
        pass


class NotifyInvitationStrategy(Strategy):
    def createNotify(self, from_user, to_user, id, describe):
        proj = Project.objects.get(pk=id)
        notify = Invitation(user=to_user,  created_datetime=datetime.now(), describe=describe, project=proj)
        notify.save()


    def setAsReaded(self, id):
        pass

