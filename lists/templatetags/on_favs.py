from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    try:
        list_models.List.objects.get(user=user)
    except list_models.List.DoesNotExist:
        list_models.List.objects.create(user=user, name="My Favourites Houses")
    the_list = list_models.List.objects.get_or_none(
        user=user, name="My Favourites Houses"
    )
    return room in the_list.rooms.all()  # boolean 반환
