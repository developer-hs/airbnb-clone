from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, Template
from django.http import HttpResponse
from . import forms

# https://docs.djangoproject.com/en/3.0/topics/auth/default/
# ↑ user
class LoginView(View):
    def get(self, request):
        form = forms.LoginForm(initial={"email": "admin@naver.com"})
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))
