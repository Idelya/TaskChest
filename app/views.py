from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm


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
    return render(request, 'projects.html')


@login_required
def notifications(request):
    return render(request, 'notifications.html')


@login_required
def statistics(request):
    return render(request, 'statistics.html')


@login_required
def tasks(request):
    return render(request, 'tasks.html')