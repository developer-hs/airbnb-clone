import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()

# takes_context =True 를 하게되면 simple_tag
# 가 context 를 받을수 있음
@register.simple_tag()
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False

