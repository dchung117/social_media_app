from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from . import views

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html") # remder home page w/ index.html