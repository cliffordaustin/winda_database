from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsUserProfile
from .serializer import UserSerializer
from user.models import CustomUser

from rest_framework.views import APIView
from allauth.account.utils import send_email_confirmation
from rest_framework import status
from rest_framework.response import Response

from rest_framework.generics import get_object_or_404
from allauth.account.admin import EmailAddress
from rest_framework.exceptions import APIException


class UserProfileView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.email

        return CustomUser.objects.filter(email=user)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserProfile]

    def get_queryset(self):
        user = self.request.user.email

        return CustomUser.objects.filter(email=user)


class EmailConfirmation(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = get_object_or_404(CustomUser, email=request.data["email"])
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            return Response(
                {"message": "This email is already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            try:
                send_email_confirmation(request, user=user)
                return Response(
                    {"message": "Email confirmation sent"},
                    status=status.HTTP_201_CREATED,
                )
            except APIException:
                return Response(
                    {
                        "message": "This email does not exist, please create a new account"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )


class CheckEmailConfirmation(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = get_object_or_404(CustomUser, email=request.data["email"])
        emailAddress = EmailAddress.objects.filter(user=user, verified=True).exists()

        if emailAddress:
            return Response(
                {"message": "This email is already verified"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "This email is not verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
