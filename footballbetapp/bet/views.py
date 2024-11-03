from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views  import LoginView
from django.http import HttpResponse

from .models import FootballTeam, MatchPrediction


# from .models import Match, MatchPrediction, FootballTeam, User

# Create your views here.

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


class LoginAppView(LoginView):
    # pass
    template_name = "bet/login.html"


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




class ProfileView(TemplateView):

    template_name = "bet/profile.html"