from django.shortcuts import render
from django.http import HttpResponse

from .models import rail_lines

def index(request):
    lines = rail_lines.objects.order_by("route_code")

    return render(request, 'index.html', {'lines': lines})

