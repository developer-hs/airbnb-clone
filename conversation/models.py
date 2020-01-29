from django.db import models
from core import models as core_models


class Conversation(core_models.TimeStampdModel):

    participants = models.ManyToManyField(
        "users.User", related_name="conversation", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)

    def count_messages(self):
        cnt_messages = self.messages.count()
        return str(cnt_messages) + " 개"

    count_messages.short_description = "Number of Message"

    def count_participants(self):
        cnt_participants = self.participants.count()
        return str(cnt_participants) + " 명"

    count_participants.short_description = "Number of Participants"


class Message(core_models.TimeStampdModel):

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says : {self.message}"
