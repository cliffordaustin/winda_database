# from django.core.mail import EmailMessage, send_mail

from anymail.message import EmailMessage
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from allauth.account.signals import email_confirmed


@receiver(user_signed_up)
def populate_profile(user, sociallogin=None, **kwargs):
    if sociallogin:
        if sociallogin.account.provider == "google":
            user_data = user.socialaccount_set.filter(provider="google")[0].extra_data
            avatar_url = user_data["picture"]

            user.avatar_url = avatar_url
            user.save()


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True

    user.save()
