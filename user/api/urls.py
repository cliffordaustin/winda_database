from django.urls import path
from .views import (
    UserProfileDetailView,
    UserProfileView,
    EmailConfirmation,
    CheckEmailConfirmation,
)

urlpatterns = [
    path("user/", UserProfileView.as_view(), name="user"),
    path("user/<int:pk>/", UserProfileDetailView.as_view(), name="user-detail"),
    path(
        "sendconfirmationemail/",
        EmailConfirmation.as_view(),
        name="send-email-confirmation",
    ),
    path(
        "checkconfirmationemail/",
        CheckEmailConfirmation.as_view(),
        name="check-email-confirmation",
    ),
]
