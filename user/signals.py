# from django.core.mail import EmailMessage, send_mail
import json
from anymail.message import EmailMessage
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from allauth.account.signals import email_confirmed
from django.conf import settings

@receiver(user_signed_up)
def populate_profile(request, user, sociallogin=None, **kwargs):
    if sociallogin:
        if sociallogin.account.provider == "google":
            user_data = user.socialaccount_set.filter(provider="google")[0].extra_data
            avatar_url = user_data["picture"]

            user.avatar_url = avatar_url
            if request.method =='POST':
                is_agent = request.POST.get('is_agent') == 'true'
                is_partner = request.POST.get('is_partner') == 'true'
                user.is_agent = is_agent
                user.is_partner = is_partner
            user.save()


@receiver(email_confirmed)
def email_confirmed_(request, email_address, **kwargs):
    user = email_address.user
    user.email_verified = True

    if (user.is_agent):
        email = user.email
        message = EmailMessage(
                to=[settings.DEFAULT_FROM_EMAIL],
            )
        message.template_id = "4982885"
        message.from_email = None
        message.merge_data = {
            email: {
                "first_name": user.first_name or "",
                "last_name": user.last_name or "",
                "user_email": user.email,
            },
        }

        message.merge_global_data = {
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "user_email": user.email,
        }
        message.send(fail_silently=True)

    user.save()
