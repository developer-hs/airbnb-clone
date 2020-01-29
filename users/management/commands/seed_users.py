from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):
    help = "This command creates many users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many users do you want to create"
        )  # 위 내용이 option 으로 들어감

    def handle(self, *args, **options):
        # print(args, options)
        print(options)
        number = options.get("number", 1)
        seeder = Seed.seeder()
        seeder.add_entity(User, number, {"is_staff": False, "is_superuser": False})
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Users created !!"))
