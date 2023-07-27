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
        
