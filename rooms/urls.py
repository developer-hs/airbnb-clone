from django.urls import path
from . import views

app_name = "rooms"

# https://docs.djangoproject.com/en/3.0/topics/http/urls/

urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]
