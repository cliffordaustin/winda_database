from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsUserProfile
from .serializer import UserSerializer, RegisterSerializer
from user.models import CustomUser

from rest_framework.views import APIView
from allauth.account.utils import send_email_confirmation
from rest_framework import status
from rest_framework.response import Response

from rest_framework.generics import get_object_or_404
from allauth.account.admin import EmailAddress
from rest_framework.exceptions import APIException
from rest_auth.views import LoginView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin


class UserProfileAPIView(RetrieveModelMixin, GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        """
        User profile
        Get profile of current logged in user.
        """
        return self.retrieve(request, *args, **kwargs)


class UserProfileView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.email

        return CustomUser.objects.filter(email=user)
    

class AgentsListView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(is_agent=True)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsUserProfile]

    def get_queryset(self):
        user = self.request.user.email

        return CustomUser.objects.filter(email=user)
    

class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save(request, invitation=True)

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"key": token.key},
            status=status.HTTP_201_CREATED,
        )


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
        
class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        # Call the parent post method to perform the default login behavior
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            # Check if the 'is_agent' parameter is provided in the request data
            is_agent = request.data.get('is_agent', False)
            is_partner = request.data.get('is_partner', False)


            if is_agent:
                user = self.user
                # Assuming you have a 'is_agent' field in your user model
                if user.is_authenticated and getattr(user, 'is_agent', False):
                    return response
                else:
                    # If the user is not an agent, return a forbidden response
                    return Response(
                        {"detail": "You are not authorized to log in as an agent.", "is_agent": False},
                        status=status.HTTP_403_FORBIDDEN
                    )
                
            if is_partner:
                user = self.user
                # Assuming you have a 'is_partner' field in your user model
                if user.is_authenticated and getattr(user, 'is_partner', False):
                    return response
                else:
                    # If the user is not an agent, return a forbidden response
                    return Response(
                        {"detail": "You are not authorized to log in as a property.", "is_partner": False},
                        status=status.HTTP_403_FORBIDDEN
                    )

        return response
