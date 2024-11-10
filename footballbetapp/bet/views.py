from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views  import (LoginView, LogoutView, 
                                        PasswordChangeView, PasswordChangeDoneView, 
                                        PasswordResetView, PasswordResetDoneView,
                                        PasswordResetConfirmView, PasswordResetCompleteView)
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect

from .models import FootballTeam, MatchPrediction


# from .models import Match, MatchPrediction, FootballTeam, User

# Create your views here.


# app views available for UNAUTHENTICATED users
class HomeView(TemplateView):
    template_name = "bet/home.html"
    # template_name = "bet/404.html"
     
    # return HttpResponse("Hello, world. You're at the polls index.")

# class BetHomeView(TemplateView):
#     template_name = "bet/home.html"


class AboutView(TemplateView):

    template_name = "bet/about.html"

    # def get(self, request):
        
        # return HttpResponse("About page")



class MatchesView(TemplateView):

    template_name = "bet/matches.html"

class TeamsView(ListView):
    model = FootballTeam
    template_name = "bet/teams.html"

class MatchView(TemplateView):

    template_name = "bet/match.html"


class RankingView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    model = MatchPrediction
    template_name = "bet/ranking.html"



# app views for authenticated users


# account/ views
class CustomLoginView(LoginView):
    template_name = "bet/registration/login.html"


class CustomLogoutView(LogoutView):
    next_page = "/login"


class CustomPasswordChangeView(PasswordChangeView):
    success_url = "/password_change/done"
    template_name = "bet/registration/password_change_form.html"    


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "bet/registration/password_change_done.html"


class CustomPasswordResetView(PasswordResetView):
    template_name = "bet/registration/password_reset_form.html"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "bet/registration/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "bet/registration/password_reset_confirm.html"
    

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "bet/registration/password_reset_complete.html"


class ProfileView(TemplateView):

    template_name = "bet/registration/profile.html"

