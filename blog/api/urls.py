from .views import *
from django.urls import path


urlpatterns = [
    path("blogs/", BlogListView.as_view(), name="blogs"),
    path("blogs/<slug>/", BlogDetailView.as_view(), name="blogs-detail"),
]
