from django import forms
from . import models


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
                self.add_error("password", form.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


# clean_password , clean_email ... 등 각각의 인자에 clean method 를 사용할 경우
# raise 를 이용해 error 를 띄어주면 되지만, 서로 연관되어있는(서로 종속되어있는) clean 만들 사용할 경우,
# self.add_error 를 통해 각자 error 를 띄어주어야한다.
