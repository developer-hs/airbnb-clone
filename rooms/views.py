from math import ceil
from django.core.paginator import Paginator
from django.shortcuts import render
from . import models


# request, response objects ↓
# https://docs.djangoproject.com/en/3.0/ref/request-response/
def all_rooms(request):
    page = request.GET.get("page")
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    return render(request, "rooms/home.html", context={"rooms": rooms},)

