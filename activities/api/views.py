from .serializers import ActivityImageSerializer, ActivitySerializer
from activities.models import Activities, ActivitiesImage
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsUserStayInstance, ObjectPermission


class ActivityCreateView(generics.CreateAPIView):
    serializer_class = ActivitySerializer
    queryset = Activities.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [ObjectPermission]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Activities.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Activities.objects.filter(slug=slug)
        return queryset


class ActivityListView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    queryset = Activities.objects.all()


class ActivityImageListView(generics.ListAPIView):
    serializer_class = ActivityImageSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = ActivitiesImage.objects.all()

        activity_slug = self.kwargs.get("activity_slug")
        if activity_slug is not None:
            activity = generics.get_object_or_404(Activities, slug=activity_slug)
            queryset = ActivitiesImage.objects.filter(activity=activity)

        return queryset


class ActivityImageCreateView(generics.CreateAPIView):
    queryset = ActivitiesImage.objects.all()
    serializer_class = ActivityImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        activity_slug = self.kwargs.get("activity_slug")
        activity = generics.get_object_or_404(Activities, slug=activity_slug)
        activity_queryset = Activities.objects.filter(slug=activity_slug, user=self.request.user)

        if not activity_queryset.exists():
            raise PermissionDenied("You can't add an image to this activity.")
        return serializer.save(activity=activity)


class ActivityImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivityImageSerializer
    permission_classes = [IsUserStayInstance]

    def get_queryset(self):

        activity_slug = self.kwargs.get("activity_slug")
        if activity_slug is not None:
            activity = generics.get_object_or_404(ActivitiesImage, slug=activity_slug)
            queryset = ActivitiesImage.objects.filter(activity=activity)

            return queryset
