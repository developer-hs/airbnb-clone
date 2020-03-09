from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.contrib.admin.utils import flatten
from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from users import models as user_models
from . import models, forms

# https://docs.djangoproject.com/en/3.0/topics/db/queries/#complex-lookups-with-q-objects
# ↑ Q object django documetation
def go_conversation(request, a_pk, b_pk):
    try:
        user_one = user_models.User.objects.get(pk=a_pk)
    except user_models.User.DoesNotExist:
        return None
    try:
        user_two = user_models.User.objects.get(pk=b_pk)
    except user_models.User.DoesNotExist:
        return None
    if user_one is not None and user_two is not None:
        try:
            conversation = models.Conversation.objects.filter(
                participants=user_one
            ).filter(participants=user_two)
            if len(list(conversation)) == 0:
                conversation = models.Conversation.objects.create()
                conversation.participants.add(user_one, user_two)
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
        conversation = list(conversation)[0]
        return redirect(
            reverse(
                "conversations:detail", kwargs={"pk": conversation.pk, "host_pk": a_pk}
            )
        )


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        host_pk = kwargs.get("host_pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        messages = models.Message.objects.filter(
            conversation__participants__pk=self.request.user.pk
        ).filter(conversation__participants__pk=host_pk)
        paginator = Paginator(messages, 5)
        page = self.request.GET.get("page")
        pageposts = paginator.get_page(page)
        return render(
            self.request,
            "conversation/conversation_detail.html",
            {"conversation": conversation, "pageposts": pageposts},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        host_pk = kwargs.get("host_pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(
            reverse("conversations:detail", kwargs={"pk": pk, "host_pk": host_pk})
        )
