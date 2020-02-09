import os
import requests
from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, Template
from django.http import HttpResponse
from . import forms, models

# https://docs.djangoproject.com/en/3.0/topics/auth/default/
# ↑ user
# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/FormView/
# ↑ FormView Attributes
class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email": "admin@naver.com"}

    def form_valid(self, form):  # if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "Nicoas",
        "last_name": "Serr",
        "email": "gygy2006@naver.com",
    }

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)


def complate_verifycation(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # to do : add succes message
    except models.User.DoseNotExsist:
        # to do : add error massage
        pass
    return redirect(reverse("core:home"))

    # https://developer.github.com/apps/building-oauth-apps/authorizing-oauth-apps/
    # ↑ gitgub Oauth documentation


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


# ↑ code 를 발급받음

# https://requests.readthedocs.io/en/master/
# ↑ requests
def github_callback(request):
    client_id = os.environ.get("GH_ID")
    client_secret = os.environ.get("GH_SECRET")
    code = request.GET.get("code", None)
    if code is not None:
        request = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )
        print(request.json())
        # ↑ token 을 발급받음 (code 필요)
    else:
        return redirect(reverse("core:home"))
