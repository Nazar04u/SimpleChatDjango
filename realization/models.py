from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError


class Thread(models.Model):
    participants = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        """Ensure exactly 2 participants before saving."""
        if self.pk and self.participants.count() > 2:
            raise ValidationError("A thread cannot have more than 2 participants.")


def validate_participants(sender, instance, action, **kwargs):
    if action in ["pre_add", "pre_set"]:
        if instance.participants.count() >= 2:
            raise ValidationError("A thread cannot have more than 2 participants.")


m2m_changed.connect(validate_participants, sender=Thread.participants.through)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
