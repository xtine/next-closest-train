from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms import model_to_dict

from datetime import datetime

from .models import rail_lines, station, StopTime

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

        # get object of closest station and convert to dictionary to return
        user_station = model_to_dict(
            station.objects.get(
                stop_lat=station_coordinates_np[min_index][0],
                stop_lon=station_coordinates_np[min_index][1],
            )
        )
        # Set parent station from id to name from stations model
        user_station["parent_station"] = str(
            rail_lines.objects.get(line_id=user_station["parent_station"])
        )

        # get all stop times for station
        user_stop_times = (
            StopTime.objects.filter(stop_id=user_station["id"])
            .order_by("departure_time")
            .filter(departure_time__gt=post_data["userTime"])[:4]
        )

        # transform stop times queryset to object
        user_stop_times_list = []

        for stop in user_stop_times:
            # format departure time from HH:MM:SS to H:M AM/PM
            readable_time = datetime.strptime(stop.departure_time, "%H:%M:%S").strftime(
                "%I:%M %p"
            )

            user_stop_times_list.append(
                {
                    "departure_time": readable_time,
                    "stop_headsign": stop.stop_headsign,
                }
            )

        # add stop times to json response
        user_station["stop_times"] = user_stop_times_list

        # Returning the POST response to JS
        return JsonResponse(user_station, safe=False)

    return render(request, "index.html", {"lines": lines})
