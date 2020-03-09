from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from . import models

# https://docs.djangoproject.com/en/3.0/ref/models/querysets/#get-or-create
# ↑ get_or_create()
# 있다면 체크하고, 없으면 생성(create) 시킴
# 특성 : boolean 일 때 생성됨 , tuple(obejct , create) 을 return
def toggle_room(request, room_pk):
    # https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/
    # ↑ manytomanyfield documentation
    action = request.GET.get("action", None)
    room = room_models.Room.objects.get_or_none(pk=room_pk)
    if room is not None and action is not None:
        # ↓ unpacking
        the_list, created = models.List.objects.get_or_create(
            user=request.user, name="My Favourites Houses"
        )
        if action == "add":
            the_list.rooms.add(room)
        if action == "remove":
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):

    template_name = "lists/list_detail.html"
