from django.urls import path
from . import views

app_name = "rooms"

# https://docs.djangoproject.com/en/3.0/topics/http/urls/

urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]
