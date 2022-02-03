import bcrypt
from django.http import request,HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
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
    #user = User.objects.get(email = request.POST['email'])
    #request.session['user_id'] = user.id
    if "user_id" not in request.session:
        return redirect("/")
    # if request.session['user_id'] == User.objects.get(email = 'frankhurtado50@gmail.com'):
    #     return redirect('/dashboard_for_admin')
    context = {
        "logged_in_user": User.objects.get(id = request.session['user_id']),
        "allSports": Sport.objects.all(),
        # add more context
    }
    return render(request, "dashboard_for_users.html", context)


def users_own_sports(request):
    context = {
        "logged_in_user": User.objects.get(id = request.session['user_id']),
    }
    return


def dashboard_for_admin(request):
    context = {
        "logged_in_user": User.objects.get(id = request.session['user_id']),
    }
    # user = User.objects.get(email = request.POST['email'])
    # request.session['user_id'] = user.id
    return render(request, '/dashboard_for_admin', context)
    #still a workin progress here, might have to make a new model


def logout(request):
    del request.session['user_id']

    return redirect("/")


def sport_search(request, sport_search, self):
    query = self.request.GET.get('q')
    object_list = Sport.objects.filter(
        Q(name__icontains=query) |
        Q(state__icontains=query)
    )
    context ={
        "sport": Sport.objects.get(id = sport_search)
    }
    return render(request, "dashboard_for_users.html", context)
    # this is a test^^^


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


def display_sport(request, self, sport_id, **kwargs):
    stuff = get_object_or_404(Sport, id=self.kwargs['sport_id'])
    context = {
        "sport": Sport.objects.get(id = sport_id),
        "logged_in_user": User.objects.get(id = request.session['user_id']),
        "total_likes":  stuff.total_likes()
    }
    return render(request, "display_sport.html", context)


# def LikeView(request, pk):
#     print(request)
#     user = User.objects.get(id = request.session['user_id'])
#     sport = get_object_or_404(Sport, id=request.POST.get('sport_id'))
#     sport.likes.add(user)
#     return HttpResponseRedirect(reverse("sports/display", args=[str(pk)]))
#     return redirect(f'sports/display/{sport_id}')


def LikeView(request, sport_id):
    print(request)
    user = User.objects.get(id = request.session['user_id'])
    sport = get_object_or_404(Sport, id=request.POST.get('sport_id'))
    sport.likes.add(user)
    #return HttpResponseRedirect(reverse("sports/display", args=[str(pk)]))
    return redirect(f'/sports/display/{sport_id}')

