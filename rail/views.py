from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        'title': '',
        'message': 'Welcome to your Django app!'
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'title': 'About',
        'message': 'This is the about page.'
    }
    return render(request, 'about.html', context)
