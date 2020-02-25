from django.urls import path
from . import views

app_name = "rooms"

# https://docs.djangoproject.com/en/3.0/topics/http/urls/

urlpatterns = [
    path("<int:pk>/", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photo/", views.RoomPhotoView.as_view(), name="photos"),
    path(
        "<int:room_pk>/photo/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete_photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
