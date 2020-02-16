from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField
from core import models as core_models

# Create your models here.


class AbstractItem(core_models.TimeStampdModel):
    """ Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):  # 편의

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):  # 시설

    """ Facility Item """

    class Meta:
        verbose_name_plural = "Facilitys"


class HouseRule(AbstractItem):  # 규칙

    """ HouseRule Model Definition"""

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampdModel):

    """ Photo Model Definition"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampdModel):

    """ Room Model """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(help_text="How many people will be staying ? ")
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilitys = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    houserules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    # https://docs.djangoproject.com/en/3.0/ref/models/instances/
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return round(all_ratings / len(all_reviews))
        return 0

    def first_photo(self):
        (photo,) = self.photos.all()[:1]
        # ↑ array 에서 unpacking
        return photo.file.url
