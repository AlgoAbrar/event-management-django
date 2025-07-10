from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='events'
    )
    image = models.ImageField(
        upload_to='event_images/',
        default='event_images/default.jpg',
        blank=True,
        null=True
    )
    participants = models.ManyToManyField(
        User,
        through='RSVP',
        related_name='rsvp_events'
    )

    def __str__(self):
        return self.name


class RSVP(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rsvps'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='rsvps'
    )
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} RSVP’d to {self.event.name}"
