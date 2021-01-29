from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
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
    return render(request, 'statistics.html')


@login_required
def tasks(request):
    return render(request, 'tasks.html')

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