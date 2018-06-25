from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("portindex/", views.register_view, name="portindex"),
    path("results/", views.results, name="results"),
    path("manageportfolio/", views.manageportfolio, name="manageportfolio"),
    path("portfolioroute/", views.portfolioroute, name="portfolioroute"),
    path("portfoliostatus/", views.portfoliostatus, name="portfoliostatus")
]
