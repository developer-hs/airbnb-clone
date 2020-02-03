from math import ceil
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from . import models


# request, response objects ↓
# https://docs.djangoproject.com/en/3.0/ref/request-response/
def all_rooms(request):
    page = request.GET.get("page", 1)
    room_list = models.Room.objects.all()
    paginator = Paginator(room_list, 10, orphans=5)
    try:
        rooms = paginator.page(page)
        return render(request, "rooms/home.html", context={"page": rooms},)
    except EmptyPage:
        return redirect("/")
    except PageNotAnInteger:
        return redirect("/")

