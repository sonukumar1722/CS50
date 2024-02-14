from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("close", views.close,name="close"),
    path("remove",views.remove,name="remove"),
    path("bid", views.bidding, name="bidding"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<str:cato>", views.category, name="category"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path("listing/<int:item_id>/comment", views.comment, name="comment"),
]
