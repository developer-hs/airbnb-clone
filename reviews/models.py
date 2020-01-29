from django.db import models
from core import models as core_models


class Review(core_models.TimeStampdModel):

    """ Review Model Difinition """

    reviews = models.TextField()
    Check_in = models.IntegerField()
    Accuracy = models.IntegerField()
    Location = models.IntegerField()
    Cleanliness = models.IntegerField()
    Value = models.IntegerField()
    Communication = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.reviews} - {self.room}"

    def rating_average(self):
        avg = (
            self.Check_in
            + self.Accuracy
            + self.Location
            + self.Cleanliness
            + self.Value
            + self.Communication
        ) / 6
        return round(avg, 2)

    rating_average.short_description = "Avg."
