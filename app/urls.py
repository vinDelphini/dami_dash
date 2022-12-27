from django.urls import path
from app.views import (
    AllUsersList,
    CurrentProfileDetailView,
    CurrentProfileUpdateView,
    InvitedUserSignup,
    ProfileDetailView,
    UserCreateView,
    UserUpdateView,
    # Dashboard
    Dashboard,
)

urlpatterns = [
    path("", CurrentProfileDetailView.as_view(), name="current-profile-detail"),
    path("users/", AllUsersList.as_view(), name="all-users-list"),
    path("signup/", InvitedUserSignup.as_view(), name="dashboard-signup"),
    path("edit/", CurrentProfileUpdateView.as_view(), name="current-profile-edit"),
    path("create/", UserCreateView.as_view(), name="admin-user-create"),
    path("<int:pk>/edit", UserUpdateView.as_view(), name="admin-user-edit"),
    path("<int:pk>/", ProfileDetailView.as_view(), name="admin-profile-detail"),
    # Dashboard
    path("dash/", Dashboard, name="dash"),
]
