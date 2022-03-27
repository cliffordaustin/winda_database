from .serializers import StaysSerializer, StayImageSerializer
from lodging.models import Stays, StayImage
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsUserStayInstance, ObjectPermission


class StaysCreateView(generics.CreateAPIView):
    serializer_class = StaysSerializer
    queryset = Stays.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class StaysDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaysSerializer
    permission_classes = [ObjectPermission]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Stays.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Stays.objects.filter(slug=slug)
        return queryset


class StaysListView(generics.ListAPIView):
    serializer_class = StaysSerializer
    queryset = Stays.objects.all()


class StayImageListView(generics.ListAPIView):
    serializer_class = StayImageSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = StayImage.objects.all()

        stay_slug = self.kwargs.get("stay_slug")
        if stay_slug is not None:
            stay = generics.get_object_or_404(Stays, slug=stay_slug)
            queryset = StayImage.objects.filter(stay=stay)

        return queryset


class StayImageCreateView(generics.CreateAPIView):
    queryset = StayImage.objects.all()
    serializer_class = StayImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        stay_slug = self.kwargs.get("stay_slug")
        stay = generics.get_object_or_404(Stays, slug=stay_slug)
        stay_queryset = Stays.objects.filter(slug=stay_slug, user=self.request.user)

        if not stay_queryset.exists():
            raise PermissionDenied("You can't add an image to this stay.")
        return serializer.save(stay=stay)


class StayImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StayImageSerializer
    permission_classes = [IsUserStayInstance]

    def get_queryset(self):

        stay_slug = self.kwargs.get("stay_slug")
        if stay_slug is not None:
            stay = generics.get_object_or_404(Stays, slug=stay_slug)
            queryset = StayImage.objects.filter(stay=stay)

            return queryset
