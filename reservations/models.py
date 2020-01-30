from django.db import models
from django.utils import timezone
from core import models as core_models


class Reservation(core_models.TimeStampdModel):

    """ Reservation Model Definition (예약)"""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending(미결)"),
        (STATUS_CONFIRMED, "Confirmed(확인)"),
        (STATUS_CANCELED, "Canceled(취소)"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservation", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservation", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out

    in_progress.boolean = True

    def is_finisehd(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finisehd.boolean = True
