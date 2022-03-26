from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserProfile
from .serializer import UserSerializer
from user.models import CustomUser


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
