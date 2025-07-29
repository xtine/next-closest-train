from django.shortcuts import render
from django.http import HttpResponse

from .models import rail_lines, station

import json


def index(request):
    lines = rail_lines.objects.order_by("route_code")

    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))

        # test print coordinates sent to backend view
        print(post_data)

    return render(request, "index.html", {"lines": lines})
