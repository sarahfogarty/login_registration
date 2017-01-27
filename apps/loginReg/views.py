from django.shortcuts import render, redirect
# what does reverse do??
from django.urls import reverse
from django.contrib import messages
from models import User
# remember no .models
# import bcrypt shoudl be in model
# import re - should be in model
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') should be in model

#   ===================CLEANED UP VERSION======================
def index(request):

    return render(request, 'loginReg/index.html')

def login(request):
    result = User.objects.validateLogin(request)

    if result[0] == False:
        # print_messages defined below
        print_messages(request, result[1])
        return redirect(reverse('index'))

    return log_user_in(request, result[1])


def register(request):
    first_name = request.POST['first_name'].lower()
    last_name = request.POST['last_name'].lower()
    user_list = User.objects.filter(first_name = first_name, last_name = last_name)
    if not user_list:
        user = User.objects.create(first_name = first_name, last_name = last_name)
    else:
        user = user_list[0]

    result = User.objects.validateReg(request)

    if result[0] == False:
        print_messages(request, result[1])
        return redirect(reverse('index'))

    return log_user_in(request, result[1])

def success(request):
    if not 'user' in request.session:
        return redirect(reverse('index'))
    return render(request, 'loginReg/success.html')


# PRINT_MESSAGES FUNCTION FROM DJANGO MESSAGES https://docs.djangoproject.com/en/1.10/ref/contrib/messages/
def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.INFO, message)

def log_user_in(request, user):
    request.session['user'] = {
        'id' : user.first_name,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
    }
    return redirect(reverse('success'))

def logout(request):
    request.session.pop('user')
    return redirect(reverse('index'))
