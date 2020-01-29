import random
from django.core.management.base import BaseCommand
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
        print(room_types, all_users)
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
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created !!"))
