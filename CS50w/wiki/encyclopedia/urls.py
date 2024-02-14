from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path ("wiki/<str:entry>", views.get_page, name = "get_page"),
    path("random", views.random_page, name = "random"),
    path("create", views.create_page, name = "create"),
    path("search", views.search_page, name= "search"),
    path("<str:entry>/edit", views.edit_page, name = "edit")
]
