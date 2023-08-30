from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from anymail.message import EmailMessage
from user.models import CustomUser
from allauth.account.views import ConfirmEmailView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_auth.registration.serializers import VerifyEmailSerializer
from rest_framework.authtoken.models import Token
from rest_auth.serializers import PasswordResetSerializer

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls.base import reverse
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_pk_to_url_str, user_username
from allauth.utils import build_absolute_uri
from dj_rest_auth.forms import AllAuthPasswordResetForm
from dj_rest_auth.serializers import PasswordResetSerializer
from rest_framework.generics import GenericAPIView


class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        user = CustomUser.objects.get(email=email)
        activate_url = (
            settings.FRONTEND_URL + "/accounts/email-verification/" + 
            context["key"] + "?redirect=/partner/agent" if user.is_agent else settings.FRONTEND_URL + "/accounts/email-verification/" + 
            context["key"] + "?redirect=/partner/lodge"
        )
        message = EmailMessage(
            to=(email, ),
        )
        message.template_id = "4977905"
        message.from_email = None
        message.merge_data = {
            email: {
                "activate_url": activate_url
            },
        }

        message.merge_global_data = {
            "activate_url": activate_url
        }
        message.send(fail_silently=True)

class VerifyEmailView(APIView, ConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ('POST', 'OPTIONS', 'HEAD')

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)
    
    def create_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)

        self.token = self.create_token(confirmation.email_address.user)

        return Response(
            {"key": self.token.key},
            status=status.HTTP_200_OK,
        )
    

class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator',
                                     default_token_generator)
        
        print("email", email)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = reverse(
                'password_reset_confirm',
                args=[user_pk_to_url_str(user), temp_key],
            )
            url = build_absolute_uri(None, path) # PASS NONE INSTEAD OF REQUEST

            print("URL: ", url)
            print("key", temp_key)
            print("site", current_site)
            print("user", user_pk_to_url_str(user))

            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }
        return self.cleaned_data['email']

class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomAllAuthPasswordResetForm
    

class PasswordResetView(GenericAPIView):
    serializer_class = CustomPasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )
        
