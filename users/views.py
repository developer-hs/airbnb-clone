import os
import requests
from django.utils import translation
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, Template, Context
from django.http import HttpResponse, HttpRequest
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from . import forms, models, mixin

# https://docs.djangoproject.com/en/3.0/topics/auth/default/
# ↑ user
# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/FormView/
# ↑ FormView Attributes
class LoginView(mixin.LoggedOutOnlyView, SuccessMessageMixin, FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    # initial = {"email": "admin@naver.com"}

    def form_valid(self, form):  # if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            messages.success(self.request, f"Hello {user.first_name}")
            login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"See you later {request.user.first_name}")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(mixin.LoggedOutOnlyView, FormView):

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
                raise GithubException("Can't get access token")
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
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )
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
                    messages.success(
                        request, f"Welcome back {user.first_name}{user.last_name}"
                    )
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get your code")
        else:
            raise GithubException()
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


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
            raise KakaoException("Can't get authorization code")
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account", None)
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException("Please also give me your email")
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        profile_image = profile.get("profile_image_url", None)
        print(profile_image)
        if profile_image is None:
            # 기본 프로필 사진 입력
            pass
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
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
        messages.success(request, f"Welcome back {user.first_name}{user.last_name}")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"
    # 유저 객체(object) 를 가르키는 방법을 바꿀수 있게해줌


# https://ccbv.co.uk/projects/Django/3.0/django.views.generic.edit/UpdateView/
# ↑ UpdateView attributes
class UpdateProfileView(mixin.LoggedOnlyView, SuccessMessageMixin, UpdateView):

    model = models.User
    template_name = "users/update_profile.html"
    fields = (
        "email",
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )
    success_message = "Profile Update"

    # UpdateView 는 기본적으로 url 의 pk 를 얻어서 그 객체의 대한 Update form 을 제공
    # 지금 하고있는 방법은 pk 를 이용하지않음으로 get_object method 수정
    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["email"].widget.attrs = {"placeholder": "Email"}
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["gender"].widget.attrs = {"placeholder": "Gender"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["language"].widget.attrs = {"placeholder": "Language"}
        form.fields["currency"].widget.attrs = {"placeholder": "Currency"}
        return form


"""     def form_valid(self, form):
        email = form.cleaned_data.get("email")
        self.object.username = email
        self.object.save()
        return super().form_valid(form) """

# https://ccbv.co.uk/projects/Django/3.0/django.contrib.auth.views/PasswordChangeView/
# ↑ PasswordChangeView Attributes
# https://docs.djangoproject.com/en/3.0/ref/contrib/messages/#adding-messages-in-class-based-views
# ↑ SuccessMessageMixin
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin
# ↑ UserPassesTestMixin
class UpdatePasswordView(
    mixin.EmailLoginOnlyView,
    mixin.LoggedOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):

    template_name = "users/update_password.html"
    success_message = "Password Update"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Cofirm new password"
        }
        return form

    def get_success_url(self):
        return self.request.user.get_absolute_url()


# https://docs.djangoproject.com/en/3.0/topics/http/sessions/#examples
# ↑ session django documentation

""" @login_required
def start_hosting(request):
    request.session["is_hosting"] = True
    return redirect(reverse("core:home"))


def stop_hosting(request):
    try:
        del request.session["member_id"]
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

    return redirect(reverse("core:home"))
     """


def switch_hosting(request):
    referer = request.META.get("HTTP_REFERER")
    try:
        del request.session["is_hosting"]
    except KeyError:
        request.session["is_hosting"] = True
    return redirect(referer)


def switch_language(request):
    lang = request.GET.get("lang", None)
    if lang is not None:
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
    return HttpResponse(status=200)
    # settings.py middleware 에 LocaleMiddleware 삽입
    # request.session 안에 translation.LANGUAGE_SESSION_KEY(_'language')
    # 를 가져와서 해당값으로 번역
    # https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#other-tags
    # ↑ templates 에 {% get_current_language as LANGUAGE_CODE %} 적용
