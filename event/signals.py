from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import RSVP


@receiver(post_save, sender=RSVP)
def send_rsvp_confirmation_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        event = instance.event
        subject = f"RSVP Confirmation for {event.name}"
        message = (
            f"Hi {user.first_name or user.username},\n\n"
            f"You have successfully booked to '{event.name}' on {event.date} at {event.time}.\n"
            f"Location: {event.location}\n\n"
            f"Thank you for joining!\n"
            f"Best Regards,\n"
            f"Saiyedul Abrar\n\n"
        )
        try:
            send_mail(
                subject,
                message,
                "saiyedul.abrar1430@gmail.com",
                [user.email],
                fail_silently=False
            )
        except Exception as e:
            print(f"Failed to send RSVP email to {user.email}: {str(e)}")
