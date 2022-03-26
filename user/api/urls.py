from django.urls import path
from .views import UserProfileDetailView, UserProfileView

urlpatterns = [
    path("user/", UserProfileView.as_view(), name="user"),
    path("user/<int:pk>/", UserProfileDetailView.as_view(), name="user-detail")
]
