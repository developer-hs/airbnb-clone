from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, Http404, render
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


class RoomDetail(DetailView):

    """ RoomDetail Definition """

    model = models.Room


def search(request):
    city = request.GET.get("city")
    city = str.capitalize(city)
    return render(request, "rooms/search.html", {"city": city})

