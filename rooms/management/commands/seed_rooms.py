import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

# https://faker.readthedocs.io/en/master/providers/faker.providers.address.html
class Command(BaseCommand):
    help = "This command creates many rooms"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many users do you want to rooms"
        )  # 위 내용이 option 으로 들어감

    def handle(self, *args, **options):
        # print(args, options)
        print(options)
        number = options.get("number", 1)
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        room_types = room_models.RoomType.objects.all()
        seeder.add_entity(
            room_models.Room,
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 10000),
                "guests": lambda x: random.randint(1, 20),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_photo = seeder.execute()
        # django_seed 는 자동으로 pk 를 증가시키지 않음
        # 대신에 seeder.execute() 를 사용하여
        # class 별로 인덱스된 pk 를 list 안에 넣어서 return 해줌
        created_clean = flatten(list(created_photo.values()))
        # ※ created_photo.values() = dict_values[[14]]
        # ※ list(created_photo.values()) = [[14]]
        # ※ flatten(list(created_photo.values())) = [14]
        # flatten = iterable 가능한 객체 (list,tuple) 를 list 에 extend 시킴
        # iterable 한 객체가 아니면 list 에 append 시킴
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"/room_photos/{random.randint(1,31)}.webp",
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilitys.add(f)
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.houserules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{number} rooms created !!"))
