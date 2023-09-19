from rest_framework import generics
from .serializers import *
from blog.models import *
from rest_framework.permissions import AllowAny


class BlogDetailView(generics.RetrieveAPIView):
    serializer_class = BlogSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Blog.objects.filter(is_active=True)
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Blog.objects.filter(slug=slug, is_active=True)
        return queryset


class BlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Blog.objects.filter(is_active=True).order_by("-id")
