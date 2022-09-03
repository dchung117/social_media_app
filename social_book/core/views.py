from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from . import views

# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Welcome to Social Book</h1>")