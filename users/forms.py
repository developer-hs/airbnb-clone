from django import forms
from . import models

# https://docs.djangoproject.com/en/3.0/topics/forms/modelforms/
# ↑ Model Form
class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                # raise form.ValidationError("Password wrong!")
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


# clean_password , clean_email ... 등 각각의 인자에 clean method 를 사용할 경우
# raise 를 이용해 error 를 띄어주면 되지만, 서로 연관되어있는(서로 종속되어있는) clean 만들 사용할 경우,
# self.add_error 를 통해 각자 error 를 띄어주어야한다.


class SignUpForm(forms.ModelForm):
    # ModelForm 에서는 clean , save method 를 지원
    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
        )
        labels = {"email": ("Email")}

    # password 암호화를 위해 따로 생성
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not math")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        # commit=False : object 가 생성되지만 database 에 적용시키지않음
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        # set_password : password 를 암호화 시켜줌
        # https://docs.djangoproject.com/en/3.0/topics/auth/default/
        # ↑ user
        user.set_password(password)
        user.save()

