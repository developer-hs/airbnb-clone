"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path("", include("core.urls"), name="core"),
    path("rooms/", include("rooms.urls"), name="rooms"),
    path("users/", include("users.urls"), name="users"),
    path("reservations/", include("reservations.urls"), name="users"),
    path("reviews/", include("reviews.urls"), name="reviews"),
    path("lists/", include("lists.urls"), name="lists"),
    path("conversations/", include("conversation.urls"), name="conversations"),
    path("admin/", admin.site.urls),
    path("sentry-debug/", trigger_error),
]

# 1번째 인자는 File_URL 2번쨰 인자는 File 저장 폴더
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
