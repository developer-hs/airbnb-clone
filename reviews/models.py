from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core import models as core_models

# https://docs.djangoproject.com/en/3.0/ref/validators/#maxvaluevalidator
# ↑ validator - django documentation
class Review(core_models.TimeStampdModel):

    """ Review Model Difinition """

    reviews = models.TextField()
    Check_in = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Accuracy = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Location = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Cleanliness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    Communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
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

    class Meta:
        ordering = ("-created",)

