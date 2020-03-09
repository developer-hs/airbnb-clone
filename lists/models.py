from django.db import models
from core import models as core_models


class List(core_models.TimeStampdModel):

    """ List Model Difinition """

    name = models.CharField(max_length=80)
    # OnetoOneField : 서로 한번씩만 가지게됨
    user = models.OneToOneField(
        "users.User", related_name="list", on_delete=models.CASCADE
    )
    rooms = models.ManyToManyField("rooms.Room", related_name="lists", blank=True)

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.rooms.count()

    count_rooms.short_description = "Number of Rooms"
