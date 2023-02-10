from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import login, authenticate, update_session_auth_hash
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import ToDoList, ToDoTask
# Create your views here.


def index(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    kontext = {
        "num_visits": num_visits,
    }
    return render(request, 'index.html', context=kontext)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class LoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse('profile')


@login_required
def list(request, list_id):
    todo_list = ToDoList.objects.get(id=list_id)
    # todo_tasks = ToDoTask.objects.filter(todolist=todo_list)
    return render(request, 'user_list.html', {'todo_list': todo_list})
@login_required
def user_to_dolist(request):
    todo_lists = ToDoList.objects.filter(user=request.user)
    return render(request, 'user_lists.html', {'todo_lists': todo_lists})
@login_required
def add_list(request):
    if request.method == 'POST':
        title = request.POST['title']
        ToDoList.objects.create(title=title, user=request.user)
        return redirect('lists')
    return render(request, 'add_list.html')

@login_required
def add_task(request, list_id):
    todo_list = ToDoList.objects.get(id=list_id)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        ToDoTask.objects.create(todo_list=todo_list, title=title, description=description)
        return redirect('list', list_id=list_id)
    return render(request, 'add_task.html', {'todo_list': todo_list})


@login_required
def complete_task(request, task_id):
    task = ToDoTask.objects.get(id=task_id)
    task.complete = True
    task.save()
    return redirect('list', task.todo_list.id)


@login_required
def delete_task(request, task_id):
    task = ToDoTask.objects.get(id=task_id)
    task.delete()
    return redirect('list', task.todo_list.id)


def delete_list(request, list_id):
    users_lists = ToDoList.objects.get(id=list_id)
    users_lists.delete()
    return redirect('lists')


@login_required
def profile_view(request):
    lists = ToDoList.objects.filter(user=request.user)
    tasks = ToDoTask.objects.filter(todo_list__in=lists)
    return render(request, 'registration/profile.html', {'lists': lists, 'tasks': tasks})


def user_list(request):
    users = User.objects.all()
    return render(request,  {'users': users})


def user_lists(request):
    users = User.objects.all()
    return render(request, 'user_lists.html', {'users': users})