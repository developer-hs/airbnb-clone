from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.HouseRule, models.Amenity)
class ItemAdmin(admin.ModelAdmin):

    """ item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.TabularInline
class PhotoInLine(admin.TabularInline):
    model = models.Photo


#                    ↑ 와 같음 보이는방식이 다름
# class PhotoInLine(admin.StackedInline):
#     model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definition """

    inlines = [
        PhotoInLine,
    ]

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "city", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book",)},),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths",)}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),
                "fields": ("amenities", "facilitys", "houserules",),
            },
        ),
        ("Last Details", {"fields": ("host",)}),
    )

    ordering = ("name", "price", "bedrooms")

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
        "created",
    )

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilitys",
        "houserules",
        "city",
        "country",
    )

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
    # ^ , = , @ 설명이 나와있음
    search_fields = ("^city", "^host__username")

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
    # ManyToManyField 에만 적용가능
    filter_horizontal = (
        "amenities",
        "facilitys",
        "houserules",
    )
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.raw_id_fields
    raw_id_fields = ("host",)

    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/

    def save_model(self, request, obj, form, change):
        print(obj, form, change)
        super().save_model(request, obj, form, change)

    # obj == row
    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    def superuser(self, obj):
        return obj.host.superhost

    # 해당하는 column name 변경
    # count_amenities.short_description = "hello sexy!"
    count_photos.short_description = "Photo_Count"


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Difinition """

    list_display = ("__str__", "get_thumnail")

    def get_thumnail(self, obj):
        # print(dir(obj.file))

        # mark_safe : django 의 각종 security 때문에 웹사이트가 javascript ,html 등
        # 각종 명령어를 읽지 못하게 막아놓은것을 풀어줌
        # ( django 에게 안전한 String 인것을 알림 )
        return mark_safe(f'<img width="50px"src="{obj.file.url}"/>')

    get_thumnail.short_description = "Thumnail"

