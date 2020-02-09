from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect, Http404, render
from django_countries import countries
from django.core.paginator import Paginator
from collections import Counter
from . import models, forms

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/
# ↑ CBV
# https://ccbv.co.uk/
# ↑ CBV property collection
# https://github.com/SmileyChris/django-countries
# ↑ django_countries


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


class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")

        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                """                     lookup filtering                    """
                # https://docs.djangoproject.com/en/3.0/ref/models/querysets/
                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price
                    # lte = Less than or equal to

                if guests is not None:
                    filter_args["guests__gte"] = guests
                    # Greater than or equal to

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["bedrooms__gte"] = beds

                if baths is not None:
                    filter_args["bedrooms__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilitys"] = facility

                qs = models.Room.objects.filter(**filter_args).order_by("price")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )

        else:
            form = forms.SearchForm()

            return render(request, "rooms/search.html", {"form": form})


def counter(models):
    """  
    a = counter(models.Room)
    for i in a:
        print(i.room_type) """

    lst = []
    model = models.objects.all()
    for m in model:
        lst.append(m)
    return lst
