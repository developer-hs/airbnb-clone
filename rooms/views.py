from django.views.generic import (
    ListView,
    DetailView,
    View,
    UpdateView,
    FormView,
    TemplateView,
)
from django.shortcuts import redirect, Http404, render, reverse, reverse
from django_countries import countries
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from collections import Counter
from . import models, forms
from users import mixin as user_mixins

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/
# ↑ CBV
# https://ccbv.co.uk/
# ↑ CBV property collection
# https://github.com/SmileyChris/django-countries
# ↑ django_countries


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    allow_empty = True
    ordering = "created"
    context_object_name = "rooms"

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(HomeView, self).dispatch(request, *args, **kwargs)
        except Http404:
            return redirect("/")


class TestView(DetailView):

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
                # https://docs.djangoproject.com/en/3.0/ref/models/querysets/#gt
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


# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/UpdateView/
# ↑ UpdateView ccbv.co.uk
class EditRoomView(user_mixins.LoggedOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilitys",
        "houserules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotoView(user_mixins.LoggedOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photo.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(request, room_pk, photo_pk):
    user = request.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Cant delete taht photo")
        else:
            models.Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Delete Photo !")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = "rooms/photo_edit.html"
    pk_url_kwarg = "photo_pk"
    success_message = "Photo Update"
    fields = ("caption",)

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedOnlyView, SuccessMessageMixin, FormView):

    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm

    # form_valid 는 http response 를 return 해야함
    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        # form 으로 room_pk 를 넘겨줌(form 에서 save 를 override 해야함)
        form.save(pk)
        messages.success(self.request, "Photo Upload")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))


class CreateRoomView(user_mixins.LoggedOnlyView, FormView):
    form_class = forms.CreateRoomForm
    template_name = "rooms/room_create.html"

    def form_valid(self, form):
        room = form.save()
        room.host = self.request.user
        room.save()
        form.save_m2m()  # 사용이유: ManyToMany Feild 는 object 가
        # data base 에 생성되지 않았으면 저장되지않는다
        messages.success(self.request, "Create Room")
        return redirect(reverse("rooms:detail", kwargs={"pk": room.pk}))

