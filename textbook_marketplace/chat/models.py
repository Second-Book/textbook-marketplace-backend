from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    name = models.CharField(max_length=255,
                            blank=False,
                            null=False)
    members = models.ManyToManyField(User,
                                     related_name='members')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_member(self, user: User) -> bool:
        return user in self.members

    def __str__(self):
        return f'Chat: {self.name} - {self.members}'


class Message(models.Model):
    chat = models.ForeignKey(Chat,
                             related_name='chat',
                             on_delete=models.CASCADE)
    sender = models.ForeignKey(User,
                               related_name='message_sender',
                               on_delete=models.CASCADE)
    receiver = models.ForeignKey('marketplace.User',
                                 related_name='message_receiver',
                                 on_delete=models.CASCADE)
    text = models.CharField(max_length=255, blank=True, null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = # TODO

    def __str__(self):
        return f'Sender_id: {self.sender.primary_key} - Text: {self.text[:10]}'
