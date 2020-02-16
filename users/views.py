import os
import requests
from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, Template
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.contrib.auth.forms import UserCreationForm
from . import forms, models

# https://docs.djangoproject.com/en/3.0/topics/auth/default/
# ↑ user
# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/FormView/
# ↑ FormView Attributes
class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    # initial = {"email": "admin@naver.com"}

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
    # https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.forms.UserCreationForm
    # form_class = UserCreationForm
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    # initial = {
    #     "first_name": "Nicoas",
    #     "last_name": "Serr",
    #     "email": "gygy2006@naver.com",
    # }

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


class GithubException(Exception):
    pass


# https://requests.readthedocs.io/en/master/
# ↑ requests
def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},  # ← json 값을 받기위해
            )
            token_json = token.json()
            # ↑ 요청한 parameters 값을 json 으로 받음 (code 값으로 token 발급)
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException()
            else:
                access_token = token_json.get("access_token")
                # ↑ token 을 발급받음 (code 필요)
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(email=email)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException()
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )
                        user.set_unusable_password()
                        # set_unusable_password() : user 의 method , User object 를 save 하지않음
                        # https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.User.set_unusable_password
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:
        # send error message
        return redirect(reverse("core:home"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException()
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account", None)
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException()
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        profile_image = profile.get("profile_image_url", None)
        print(profile_image)
        if profile_image is None:
            # 기본 프로필 사진 입력
            pass
        try:
            user = models.User.objects.get(email=email)
            if user.login_method == models.User.LOGIN_KAKAO:
                pass
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:
                photo_request = requests.get(profile_image)
                # https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.FileField
                # FieldFile.save 의 인자는 name , content 여기서 content 는 파일을 의미
                user.avatar.save(
                    f"{nickname}-avatar.jpg",
                    ContentFile(photo_request.content)
                    # photo_request.content() 는 byte 임 파일로 이것을 파일로 담기위해
                    # ContentFile 을 사용
                    # avatar 는 FieldFile 에 속하기 때문에 user.save() 불필요(알아서저장됨)
                )
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException:
        return redirect(reverse("users:login"))
