from django.shortcuts import render, redirect
from django.http import HttpResponse
#from base.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
# Create your views here.

from django.contrib.auth import get_user_model
User = get_user_model()


def loginPage(request):
    page = 'login'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('orders:home')
            else:
                messages.error(request, 'Username or password does not exist')
        except:
            messages.error(request, 'User does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('base:home')


def registerUser(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('stocks:home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

# We mostly don't need this
# def userProfile(request, pk):
#     user = User.objects.get(id=pk)
#     context = {'user': user}
#     return render(request, 'base/profile.html', context)


def home(request):
    return render(request, 'home.html')
