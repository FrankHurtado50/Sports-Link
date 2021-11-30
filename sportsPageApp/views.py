import bcrypt
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *


# Create your views here.
def index(request):
    return render(request, "reg_page.html")


def register_info(request):
    print(request)
    errors = User.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        hash_slasher = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_account = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_slasher
        )

        request.session['user_id'] = new_account.id
        return redirect('/dashboard')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    #if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/dashboard')


def dashboard(request):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "logged_in_user": User.objects.get(id = request.session['user_id']),
        # add more context
    }
    return render(request, "dashboard.html", context)
