import csv
from django.core.exceptions import PermissionDenied

from django.shortcuts import render
from django.http import HttpResponse
from .models import SingleTrip

# Create your views here.


def export(request):
    if not request.user.is_staff:
        raise PermissionDenied
    response = HttpResponse(content_type="text/csv")

    writer = csv.writer(response)
    writer.writerow(["name", "is_active"])

    for trip in SingleTrip.objects.all().values_list("name", "is_active"):
        writer.writerow(trip)

    response["Content-Dispositon"] = 'attachment; filename="trips.csv"'

    return response
