import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from conversation import models as conversation_models
from users import models as user_models

NAME = "conversations"


class Command(BaseCommand):
    help = f"This command creates many {NAME}"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            default=1,
            type=int,
            help=f"How many {NAME} do you want to create",
        )  # 위 내용이 option 으로 들어감

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(conversation_models.Conversation, number)
        created = seeder.execute()
        cleaned = flatten(list(created.values()))
        users = user_models.User.objects.all()
        for pk in cleaned:
            conversation = conversation_models.Conversation.objects.get(pk=pk)
            conversation.participants.add(users[0])  # admin 추가
            for i in range(0, random.randint(2, 5)):
                magic_number = random.randint(1, len(users))
                conversation.participants.add(users[magic_number])

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created !!"))
