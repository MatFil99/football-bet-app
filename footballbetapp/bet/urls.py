from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    # path("home/", views.BetHomeView.as_view(), name="bethome"),
    path("about/", views.AboutView.as_view(), name="about"),
    # path("login/", views.LoginView.as_view(), name="login"),
    path("matches/", views.MatchesView.as_view(), name="matches"),
    path("teams/", views.TeamsView.as_view(), name="teams"),
    # path("matches/<int:match_id>", views.index, name="index"),
    path("ranking/", views.RankingView.as_view(), name="ranking"),


    # authorization views
    path("profile/", views.ProfileView.as_view(), name="profile"),

    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.CreateUserView.as_view(), name="register"),

    path("password_change/", views.CustomPasswordChangeView.as_view(), name="password_change"),
    path("password_change/done", views.CustomPasswordChangeDoneView.as_view(), name="password_change_done"),
    
    path("password_reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]