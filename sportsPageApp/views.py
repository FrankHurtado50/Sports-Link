import bcrypt
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *


# Create your views here.
def index(request):
    return render(request, "index.html")


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
