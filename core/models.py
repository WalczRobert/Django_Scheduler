from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model


class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=255)

    def __str__(self):
        return "{} <{}>".format(self.name, self.email)


class Schedule(models.Model):
    REASONS = (
        (1, "Vacation"),
        (2, "Training"),
        (3, "Work Travel"),
        (4, "FMLA"),
        (5, "Development"),
        (6, "Other"),
    )
    start_date = models.DateField()
    end_date = models.DateField()
    created_on = models.DateField(auto_now_add=True)
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='schedules')
    reason = models.IntegerField(choices=REASONS, default=1)


class AdminSetting(models.Model):
    max_out = models.IntegerField(default=1)


@receiver(post_save, sender=Schedule)
def notify_by_email(sender, instance, created, **kwargs):
    if created:
        emails = [instance.person.email]
        for u in get_user_model().objects.all():
            emails.append(u.email)
        all_emails = list(set(emails+settings.ADDITIONAL_EMAILS))
        delta = instance.end_date - instance.start_date
        days = delta.days+1
        for d in range(days):
            send_mail(
                'Subject here',
                'Here is the message.',
                settings.DEFAULT_FROM_EMAIL,
                all_emails,
                fail_silently=False,
            )
