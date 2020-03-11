from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = "This command creates superuser"

    def handle(self, *args, **options):
        try:
            admin = User.objects.get(username="ebadmin")
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))
        except User.DoesNotExist:
            User.objects.create_superuser("ebadmin", "gygy2006@naver.com", "admin")
            self.stdout.write(self.style.SUCCESS(f"superuser Creasted"))

