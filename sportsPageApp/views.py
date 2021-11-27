from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    print("testing method")
    return HttpResponse("testing method")
