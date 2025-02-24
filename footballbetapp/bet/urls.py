from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(http_method_names=["get"]), name="home"),
    path("contact/", views.ContactView.as_view(http_method_names=["get", "post"]), name="contact"),
    path("contact/success", views.ContactSuccessView.as_view(http_method_names=["get"]), name="contact_success"),
    path("about/", views.AboutView.as_view(http_method_names=["get"]), name="about"),
    # path("login/", views.LoginView.as_view(), name="login"),
    path("teams/", views.TeamsView.as_view(http_method_names=["get","post"]), name="teams"),
    path("matches/", views.MatchesView.as_view(http_method_names=["get","post"]), name="matches"),
    path("matches/<int:match_id>", views.MatchView.as_view(), name="match"),
    path("matches/<int:match_id>/comment", views.MatchCommentView.as_view(), name="comment_match"),
    
    path("matches/<int:match_id>/predict", views.MatchPredictView.as_view(), name="predict"),
    # path("matches/<int:match_id>", views.MatchCommentView.as_view(http_method_names=["get","post"]), name="comment_match"),
    path("ranking/", views.RankingView.as_view(), name="ranking"),

    # authorization views
    path("profile/", views.ProfileView.as_view(), name="profile"),

    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("register/<str:registration_code>", views.ActivateAccount.as_view(), name="activate_account"),

    path("password_change/", views.CustomPasswordChangeView.as_view(), name="password_change"),
    path("password_change/done", views.CustomPasswordChangeDoneView.as_view(), name="password_change_done"),
    
    path("password_reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),

    path("password_reset/done/", views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # admin views
    path("matches/load_results/", views.LoadMatchesResults.as_view(), name="load_matches_results"),
    path("matches/calculate_predictions_points/", views.CalculatePredictionsPoints.as_view(), name="calculate_predictions_points"),
    
]