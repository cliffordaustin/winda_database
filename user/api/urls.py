from django.urls import path
from .views import (
    UserProfileDetailView,
    UserProfileView,
    EmailConfirmation,
    CheckEmailConfirmation,
    AgentsListView,
)

urlpatterns = [
    path("user/", UserProfileView.as_view(), name="user"),
    path("agents/", AgentsListView.as_view(), name="agents"),
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
