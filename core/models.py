from django.db import models


class TimeStampdModel(models.Model):

    """ Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # auto_now : Save 할 때 date , time 기록
    # auto_now_add : Model 생성할 때 기록
    class Meta:
        abstract = True  # database 에 등록되는것을 허용하지않음

