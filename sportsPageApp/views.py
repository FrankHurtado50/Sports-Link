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


def logout(request):
    del request.session['user_id']

    return redirect("/")


def new_sport(request):
    context = {
        "logged_in_user": User.objects.get(id = request.session['user_id'])
    }
    return render(request, "creating_sports.html", context)


def create_sport(request):
    errors = Sport.objects.sport_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/sports/new")
    else:
        this_sport = User.objects.get(id = request.session['user_id'])
        Sport.objects.create(
            sport_name = request.POST['sport_name'],
            description = request.POST['description'],
            city = request.POST['city'],
            day_of_week = request.POST['day_of_week'],
            time = request.POST['time'],
            creator = this_sport
        )
        return redirect("/dashboard")


def remove_sport(request, sport_id):
    sport = Sport.objects.get(id = sport_id)
    sport.delete()
    return redirect('/dashboard')


def edit_sport(request, sport_id):
    context = {
        "sport": Sport.object.get(id = sport_id),
        "logged_in_user": User.objects.get(id = request.session['user_id'])
    }
    return render(request, "edit_sports.html", context)


def update_sport(request, sport_id):
    errors = Sport.objects.sport_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/sports/edit/{sport_id}")
    else:
        sport = Sport.objects.get(id = sport_id)
        sport.sport_name = request.POST['sport_name'],
        sport.description = request.POST['description'],
        sport.city = request.POST['city'],
        sport.day_of_week = request.POST['day_of_week'],
        sport.time = request.POST['time'],
        sport.save()

        return redirect('/dashboard')


def display_sport(request, sport_id):
    context = {
        "sport": Sport.objects.get(id = sport_id),
        "logged_in_user": User.objects.get(id = request.session['user_id'])
    }
    return render(request, "display_sport.html", context)

