from allauth.account.signals import user_signed_up
from django.dispatch import receiver


@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):
    if sociallogin.account.provider == "google":
        user_data = user.socialaccount_set.filter(provider="google")[0].extra_data
        avatar_url = user_data["picture"]

    user.avatar_url = avatar_url
    user.save()
