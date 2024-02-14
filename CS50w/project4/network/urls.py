
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:user_id>", views.profile, name='profile'),
    path("follow/<int:user_id>", views.follow, name='follow'),
    path("following", views.following, name='following'),
    path("edit", views.edit, name='edit_post'),
    path("like", views.like, name='like')
]
