from rest_framework import generics
from .serializers import *
from blog.models import *


class BlogDetailView(generics.RetrieveAPIView):
    serializer_class = BlogSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Blog.objects.all()
        slug = self.kwargs.get("slug")

        if slug is not None:
            queryset = Blog.objects.filter(slug=slug)
        return queryset


class BlogListView(generics.ListAPIView):
    serializer_class = BlogSerializer

    def get_queryset(self):
        return Blog.objects.all()