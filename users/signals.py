from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.SITE_URL}/activate/{instance.id}/{token}/"

        subject = 'Activate Your Account'
        message = (
            f"Hi {instance.username},\n\n"
            f"Please activate your account by clicking the link below:\n"
            f"{activation_url}\n\n"
            f"Thank you!"
        )
        recipient_list = [instance.email]

        try:
            send_mail(
                subject,
                message,
                f"saiyedul.abrar1430@gmail.com",
                recipient_list,
                fail_silently=False
            )
        except Exception as e:
            print(f"Activation email failed to send to {instance.email}: {str(e)}")


@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created:
        participant_group, _ = Group.objects.get_or_create(name='Participant')
        instance.groups.add(participant_group)
