from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # path("home/", views.BetHomeView.as_view(), name="bethome"),
    path("about/", views.AboutView.as_view(), name="about"),
    # path("login/", views.LoginAppView.as_view(), name="login"),
    path("matches/", views.MatchesView.as_view(), name="matches"),
    path("teams/", views.TeamsView.as_view(), name="teams"),
    # path("matches/<int:match_id>", views.index, name="index"),
    path("ranking/", views.RankingView.as_view(), name="ranking"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]