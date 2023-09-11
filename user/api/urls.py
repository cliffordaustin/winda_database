from django.urls import path
from .views import (
    UserProfileDetailView,
    UserProfileView,
    EmailConfirmation,
    CheckEmailConfirmation,
    AgentsListView,
    CreateUserView,
    UserProfileAPIView
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

    path("user/registration/create/", CreateUserView.as_view(), name="create-user"),
    path('user-profile/', UserProfileAPIView.as_view(), name='user-profile'),
]
