import datetime
from django.db import models
from django.utils import timezone
from django.contrib import messages
from core import models as core_models
from django.utils.translation import gettext_lazy as _


class BookedDay(core_models.TimeStampdModel):

    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)


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

    def is_finished(self):
        now = timezone.now().date()
        is_finished = now > self.check_out
        if is_finished and self.status == "canceled":
            self.delete()
        return is_finished

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        if True:  # 새로운 Reservation 일 경우
            start = self.check_in
            end = self.check_out
            difference = end - start
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end), reservation__room=self.room
            ).exists()
            if not existing_booked_day:
                super().save(*args, **kwargs)
                for i in range(difference.days + 1):
                    day = start + datetime.timedelta(days=i)
                    BookedDay.objects.create(day=day, reservation=self)
                return
        return super().save(*args, **kwargs)

