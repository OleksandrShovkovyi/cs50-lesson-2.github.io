from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("archive", views.archive, name="archive"),
    path("favorites", views.favorites, name="favorites"),
    path("cat/<str:cat>", views.category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("close/<int:id>", views.close, name="close"),
    path("lot/<int:id>", views.lot, name="lot"),
    path("wish/<int:id>", views.wish, name="wish"),
    path("comment/<int:id>", views.comment, name="comment")
]
