from django.shortcuts import render

from django.http import HttpResponse, HttpRequest
import re

from django.utils.timezone import datetime
from django.http import HttpResponse

def hello_there(request: HttpRequest, name: str):
    return render(
        request,
        'hello/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def home(request: HttpRequest):
    return render(request, "hello/home.html")

def about(request: HttpRequest):
    return render(request, "hello/about.html")

def contact(request: HttpRequest):
    return render(request, "hello/contact.html")