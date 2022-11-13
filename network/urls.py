
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createPost, name="create"),
    path("edit/<int:post_id>/<str:edit>", views.edit, name="edit"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("calendar", views.calendar, name="calendar"),
    path("resources", views.resources, name="resources"),
]
