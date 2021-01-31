from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from .forms import SignUpForm, MembershipFormset, NewProjectForm, NewTableForm, TaskCreateForm, LogTimeForm
from .models import Project, Membership, User, Table, Assign
from django.core.exceptions import PermissionDenied
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView
from .models import Task
from .lib import calcTimeForTask, getMonthStatistics
from json import dumps 

def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'index.html')
    else:
        form = AuthenticationForm()
    return render(request, 'index.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
         return redirect('index')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def projects(request):
    memberships = Membership.objects.filter(user_id=request.user.id)
    created = memberships.filter(isCreator=True).values('project_id')
    participant = memberships.filter(isCreator=False, status='A').values('project_id')
    invitations = memberships.filter(isCreator=False, status='U').values('project_id')

    user_projects_list = Project.objects.filter(id__in=created)
    
    user_participant_list = Project.objects.filter(id__in=participant)
    user_invitations_list = Project.objects.filter(id__in=invitations)
    context = {'user_projects_list': user_projects_list, 'user_participant_list': user_participant_list, 'user_invitations_list': user_invitations_list}
    return render(request, 'projects.html', context)


@login_required
def notifications(request):
    return render(request, 'notifications.html')


@login_required
def statistics(request):
    #statistics - month of user
    labels = []
    data = []
    memberships = Membership.objects.filter(user_id=request.user.id, status='A').values('project_id')

    user_projects_list = Project.objects.filter(id__in=memberships)

    month_data = getMonthStatistics(request.user)

    context = {'projects': user_projects_list, 'month_data': dumps(month_data)}
    return render(request, 'statistics.html', context) 


@login_required
def tasks(request):
    assigned_tasks = Assign.objects.filter(user_id=request.user.id).values('task_id')
    tasks = Task.objects.filter(pk__in = assigned_tasks)
    
    context = {'tasks': calcTimeForTask(tasks, request.user.id)}
    return render(request, 'tasks.html', context)

@transaction.atomic
@login_required
def newproject(request):
    if request.method == 'GET':
        projectForm = NewProjectForm(request.GET or None)
        formset = MembershipFormset()
    elif request.method == 'POST':
        projectForm = NewProjectForm(request.POST)
        formset  = MembershipFormset(request.POST)

        if formset.is_valid() and projectForm.is_valid():
            proj = projectForm.save()
            creator = Membership(status='A', user=request.user, project=proj, isCreator=True)
            creator.save()

            foms = list(set(map(lambda f: f.cleaned_data.get('username'),formset)))
            for username in foms:
                try:
                    if username!=request.user.username:
                        user = User.objects.get(username=username)
                        if user is not None:
                            member = Membership(status='U', user=user, project=proj, isCreator=False)
                            member.save()
                except:
                    print("Not found")
        return redirect('projects')
    return render(request, 'newproject.html', {
        'projectForm':projectForm,
        'formset': formset,
    })

@login_required
def invitationAccept(request):
    post = get_object_or_404(Membership, project_id=10, user=request.user)
    post.status = 'A'
    post.save()
    return redirect('projects')

    
@login_required
def invitationDiscard(request):
    post = get_object_or_404(Membership, project_id=10, user=request.user)
    post.status = 'R'
    post.save()
    return redirect('projects')


@login_required
def projectManage(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
            tableFrom = NewTableForm(request.POST)
            if tableFrom.is_valid():
                table = tableFrom.save(commit=False)
                table.project_id = id
                table.save()
                return redirect('projectManage', id)

    tableForm = NewTableForm(request.GET or None)
    check = Membership.objects.filter(project_id=id, user=request.user,status='A').exists()
    if not check:
        raise PermissionDenied
    tables = Table.objects.filter(project_id=id)

    for tab in tables:
        tab.tasks = Task.objects.filter(table_id=tab.id)

    context = {'project': project, 'project_tables': tables, 'table_form': tableForm}

    project = get_object_or_404(Membership, project_id=id, user=request.user)
    return render(request, 'manageproject.html', context)


@login_required
def taskCreate(request, id):
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        form = TaskCreateForm(request.POST, project_id=id)
        print(form.is_valid())
        if form.is_valid():
            print(form)
            task = form.save(commit=False)
            task.project_id = id
            task.save()
            users = form.cleaned_data['assigned_users']
            for user in users:
                user = Assign(user=user,task_id=task.id)
                user.save()

            return redirect('projectManage', id)
        else:
            print(form.errors)


    check = Membership.objects.filter(project_id=id, user=request.user,status='A').exists()
    if not check:
        raise PermissionDenied
    tables = Table.objects.filter(project_id=id)
    
    taskForm = TaskCreateForm(request.GET or None, project_id=id)

    
    context = {'project': project, 'project_tables': tables, 'task_form': taskForm}

    project = get_object_or_404(Membership, project_id=id, user=request.user)
    return render(request, 'manageproject.html', context)


@login_required
def taskView(request, id):
    task = get_object_or_404(Task, id=id)
    project = get_object_or_404(Project, id=task.project_id)
    check = Membership.objects.filter(project_id=project.id, user=request.user,status='A').exists()
    if not check:
        raise PermissionDenied
    tables = Table.objects.filter(project_id=project.id)

    context = {'project': project, 'project_tables': tables, 'task': task}

    return render(request, 'manageproject.html', context)


@login_required
def taskEdit(request, id):
    task = get_object_or_404(Task, id=id)
    project = get_object_or_404(Project, id=task.project_id)
    if request.method == 'POST':
        form = TaskCreateForm(request.POST, instance=task, project_id=task.project_id)
        if form.is_valid():
            task = form.save()
            
        return redirect('projectManage', task.project_id)


    check = Membership.objects.filter(project_id=task.project_id, user=request.user,status='A').exists()
    if not check:
        raise PermissionDenied
    tables = Table.objects.filter(project_id=task.project_id)
    
    taskForm = TaskCreateForm(request.GET or None, instance=task, project_id=task.project_id)

    
    context = {'project': project, 'project_tables': tables, 'task_form': taskForm}

    return render(request, 'manageproject.html', context)


@login_required
def logTime(request, id):
    task = get_object_or_404(Task, id=id)
    project = get_object_or_404(Project, id=task.project_id)
    check = Membership.objects.filter(project_id=task.project_id, user=request.user,status='A').exists()
    if not check:
        raise PermissionDenied

    if request.method == 'POST':
        form = LogTimeForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user_id = request.user.id
            log.task_id = task.id
            log.save()
        return redirect('projectManage', task.project_id)
    tables = Table.objects.filter(project_id=task.project_id)
    logTimeForm = LogTimeForm(request.GET or None)
    context = {'project': project, 'project_tables': tables, 'log_time_form': logTimeForm}

    return render(request, 'manageproject.html', context)
