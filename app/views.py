from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, MembershipFormset, NewProjectForm
from .models import Project, Membership, User


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
    user_projects_list = Project.objects.all()
    context = {'user_projects_list': user_projects_list}
    return render(request, 'projects.html', context)


@login_required
def notifications(request):
    return render(request, 'notifications.html')


@login_required
def statistics(request):
    return render(request, 'statistics.html')


@login_required
def tasks(request):
    return render(request, 'tasks.html')


@login_required
def newproject(request):
    if request.method == 'GET':
        projectForm = NewProjectForm(request.GET or None)
        formset = MembershipFormset()
    elif request.method == 'POST':
        print('post')
        projectForm = NewProjectForm(request.POST)
        formset  = MembershipFormset(request.POST)
        print(formset.is_valid())
        if formset.is_valid() and projectForm.is_valid():
            proj = projectForm.save()
            creator = Membership(status='A', user=request.user, project=proj, isCreator=True)
            creator.save()
            for form in formset:
                username = form.cleaned_data.get('username')
                if username!=request.user.username:
                    user = User.objects.get(username=username)
                    if user is not None:
                        member = Membership(status='U', user=user, project=proj, isCreator=False)
                        member.save()
        return redirect('projects')
    return render(request, 'newproject.html', {
        'projectForm':projectForm,
        'formset': formset,
    })