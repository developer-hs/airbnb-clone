from django.views.generic import ListView
from django.shortcuts import render, redirect, Http404
from . import models

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/
# https://ccbv.co.uk/


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    allow_empty = True
    ordering = "created"
    context_object_name = "rooms"

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(HomeView, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect("/")


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        raise Http404()
