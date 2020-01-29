from django.core.management.base import BaseCommand
from rooms.models import Facility


class Command(BaseCommand):
    help = "This command creates facilities"
    """ 
        def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell you that I Love You?"
        )  """

    def handle(self, *args, **options):
        # print(args, options)
        facilities = [
            "Washing machine",
            "Dryer",
            "Breakfast",
            "Indoor fireplace",
            "Cot",
            "High chair",
            "Self check_in",
            "Free parking on premises",
            "Gym",
            "Hot tub",
            "Pool",
        ]

        for a in facilities:
            Facility.objects.create(name=a)
        self.stdout.write(
            self.style.SUCCESS(f"{len(facilities)} facilities created !!")
        )
