from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views  import (LoginView, LogoutView, 
                                        PasswordChangeView, PasswordChangeDoneView, 
                                        PasswordResetView, PasswordResetDoneView,
                                        PasswordResetConfirmView, PasswordResetCompleteView)
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect


from .models import FootballTeam, MatchPrediction, User, Match
from .forms import CustomUserCreationForm


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



class MatchesView(ListView):
    queryset = Match.objects.all() #.order_by("date")

    template_name = "bet/matches.html"

class TeamsView(ListView):
    # model = FootballTeam
    queryset = FootballTeam.objects.all().order_by("name")
    template_name = "bet/teams.html"

class MatchView(TemplateView):

    template_name = "bet/match.html"


# class RankingView(PermissionRequiredMixin, ListView):
#     permission_required = []
class RankingView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    model = MatchPrediction
    template_name = "bet/ranking.html"
    



# app views for authenticated users




# account/registration views
class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "bet/registration/profile.html"


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


class CreateUserView(FormView):
    form_class = CustomUserCreationForm
    success_url = "/login"
    template_name = "bet/registration/register.html"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")

        print(username)
        print(first_name)
        print(last_name)
        print(email)
        print(password)

        User.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
        )
        
        return super().form_valid(form)