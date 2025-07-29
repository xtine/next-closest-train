from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms import model_to_dict

from .models import rail_lines, station

import json
import numpy as np


def index(request):
    # Grab Metro rail line info to display to user
    lines = rail_lines.objects.order_by("route_code")

    # "Locate Me" button request
    if request.method == "POST":
        post_data = json.loads(request.body.decode("utf-8"))

        station_coordinates = []

        # load array of station coordinates
        for s in station.objects.all():
            station_coordinates.append([s.stop_lat, s.stop_lon])

        # Put all the station coordinates into NumPy array
        station_coordinates_np = np.array(station_coordinates)

        # Set user coordinate into NumPy array
        user_coordinates_np = np.array((post_data["lat"], post_data["lon"]))

        # Calculating Euclidean Distance between two points
        distances = np.linalg.norm(station_coordinates_np - user_coordinates_np, axis=1)
        min_index = np.argmin(distances)

        # get object of closest station
        user_station = model_to_dict(
            station.objects.get(
                stop_lat=station_coordinates_np[min_index][0],
                stop_lon=station_coordinates_np[min_index][1],
            )
        )

        # Convert Django object to dict to return
        user_station["parent_station"] = str(
            rail_lines.objects.get(line_id=user_station["parent_station"])
        )

        # Returning the POST response to JS
        return JsonResponse(user_station, safe=False)

    return render(request, "index.html", {"lines": lines})
