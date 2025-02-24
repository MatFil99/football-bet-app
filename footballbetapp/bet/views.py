from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views  import (LoginView, LogoutView, 
                                        PasswordChangeView, PasswordChangeDoneView, 
                                        PasswordResetView, PasswordResetDoneView,
                                        PasswordResetConfirmView, PasswordResetCompleteView)

from django.http import HttpResponse
from django.shortcuts import redirect

from django.urls import reverse, reverse_lazy

from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.conf import settings

# to remove
from django.contrib.sites.shortcuts import get_current_site


from .models import FootballTeam, MatchPrediction, User, Match, MatchComment
from .forms import CustomUserCreationForm, StandingsForm, MatchesForm, MatchCommentForm, MatchPredictionForm, ContactForm


import subprocess

# from .models import Match, MatchPrediction, FootballTeam, User

# Create your views here.


# app views available for UNAUTHENTICATED users
class HomeView(TemplateView):
    template_name = "bet/home.html"


class AboutView(TemplateView):

    template_name = "bet/about.html"


class MatchesView(ListView, FormMixin):
    queryset = Match.objects.all() #.order_by("date")
    template_name = "bet/matches.html"
    form_class = MatchesForm

    # def _

    def get(self, request, *args, **kwargs):
        default_league = "premier-league"
        default_season = Match.get_current_season(default_league)
        default_season = "2024/2025" if default_season is None else default_season
        default_matchday = Match.get_current_matchday(default_league, default_season)
        default_matchday = 1 if default_matchday is None else default_matchday
        
        context = self._prepare_context(league=default_league, season=default_season, matchday=default_matchday)
        
        return render(request, MatchesView.template_name ,context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        league = form.data["league"]
        season = form.data["season"]
        matchday = int(form.data["matchday"])

        context = self._prepare_context(league=league, season=season, matchday=matchday)

        return render(request, MatchesView.template_name ,context)


    def _prepare_context(self, league: str, season: str, matchday: int):
        """
        """
        matches = Match.objects.filter(home_team__league=league).filter(season=season).filter(matchday=matchday) | \
            Match.objects.filter(home_team__league=league).filter(season=season).filter(matchday=matchday)
        matches = matches.order_by("date")
        matchdays = Match.objects.order_by("matchday").values_list("matchday", flat=True).distinct()
        seasons = Match.objects.values_list("season", flat=True).distinct()
        leagues = FootballTeam.objects.values_list("league", flat=True).distinct()

        context = {
            "object_list": matches,
            "league_list": leagues,
            "season_list": seasons,
            "matchday_list": matchdays,
            "selected_league": league,
            "selected_season": season,
            "selected_matchday": matchday,
        }
        return context

class TeamsView(ListView, FormMixin):
    template_name = "bet/teams.html"
    form_class = StandingsForm

    def get(self, request, *args, **kwargs):
        default_league = "premier-league"
        default_season = "2024/2025"

        context = self._prepare_context(league=default_league, season=default_season)

        return render(request, TeamsView.template_name ,context)
    
    def post(self, request, *args, **kwargs):
        # self.Form(self.request.POST)
        form = self.get_form()
        league = form.data['league'] if form.data['league'] is not None else "premier-league"
        season = form.data['season'] if form.data['season'] is not None else "2024/2025"

        context = self._prepare_context(league=league, season=season)

        return render(request, TeamsView.template_name ,context)

    def _prepare_context(self, league, season):
        try:
            teams_standings = FootballTeam.get_teams_stats(league=league, season=season)
        except:
            teams_standings = None

        leagues = FootballTeam.objects.values_list("league", flat=True).distinct()
        seasons = Match.objects.values_list("season", flat=True).distinct()
    
        context = {
            "object_list": teams_standings,
            "league_list": leagues,
            "season_list": seasons,
            "selected_league": league,
            "selected_season": season
        }

        return context


class MatchView(DetailView):
    template_name = "bet/match.html"
    model = Match
    comments_model = MatchComment
    context_object_name = "match"
    context_comments = "comments"
    pk_url_kwarg = "match_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        match_prediction = None
        match = kwargs["object"]
        comments = MatchView.comments_model.get_match_comments(match.match_id)

        user = self.request.user
        if user.is_authenticated:
            match_prediction = MatchPrediction.get_user_match_prediction(user, match)
        context["match_prediction"] = match_prediction
        context[MatchView.context_comments] = comments

        return context

class MatchCommentView(LoginRequiredMixin, FormView):
    # template_name = "bet/match.html"
    login_url = "/login/"
    success_url = "match"

    form_class = MatchCommentForm

    def post(self, *args, **kwargs):
        form = self.get_form()
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            match_id = kwargs["match_id"]
            comment_text = form.data["text"]
            
            user = User.objects.get(id=user_id)
            match = Match.objects.get(match_id=match_id)
            comment = MatchComment.create(
                author=user,
                match=match,
                text=comment_text
                )
        else:
            print("Not authenticated")

        return redirect(reverse(MatchCommentView.success_url, kwargs=kwargs))

class MatchPredictView(LoginRequiredMixin, FormView):
    login_url = "/login/"
    form_class = MatchPredictionForm
    success_url = "match"

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            match = Match.objects.get(match_id=kwargs["match_id"])
            if not match.match_played_or_started() or True: # comment out the True
                user = self.request.user
                home_score = form.data["home_score"] if form.data["home_score"]!="" else None
                away_score = form.data["away_score"] if form.data["away_score"]!="" else None
                mp = MatchPrediction.get_user_match_prediction(user, match)

                if mp is None:
                    mp = MatchPrediction(user=user, match=match, home_score_prediction=home_score, away_score_prediction=away_score)
                    mp.save()
                else:
                    mp.update_prediction(home_score=home_score, away_score=away_score)
            else:
                pass # match was played or started, can't make a bet
                
        # stay on the same page
        return redirect(reverse(MatchPredictView.success_url, kwargs=kwargs))

class RankingView(LoginRequiredMixin, ListView):
    login_url = "/login/"
    model = MatchPrediction
    template_name = "bet/ranking.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ranking = MatchPrediction.get_ranking()
        context["ranking"] = ranking
        return context


# app views for authenticated users


class ContactView(LoginRequiredMixin, FormView):
    login_url = "/login/"
    template_name = "bet/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_success")

    def form_valid(self, form):
        form.send()
        return super().form_valid(form)

class ContactSuccessView(TemplateView):
    template_name = "bet/success.html"

# account/registration views
class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = "/login"
    template_name = "bet/registration/profile.html"


class CustomLoginView(LoginView):
    template_name = "bet/registration/login.html"


class CustomLogoutView(LogoutView):
    next_page = "/login"


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    login_url = "/login/"
    success_url = "/password_change/done"
    template_name = "bet/registration/password_change_form.html"    


class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "bet/registration/password_change_done.html"


class CustomPasswordResetView(PasswordResetView):
    template_name = "bet/registration/password_reset_form.html"
    email_template_name = "bet/registration/password_reset_email.html"
    from_email = settings.EMAIL_HOST_USER


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "bet/registration/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "bet/registration/password_reset_confirm.html"
    

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    # template_name = "bet/registration/password_reset_complete.html"

    def get(self, request, *args, **kwargs):
        return redirect("login")


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

        user = User.objects.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password,
        )
        
        return super().form_valid(form)
    

class ActivateAccount(TemplateView):
    template_name = "bet/registration/account_activation.html"
    

    def get_context_data(self, **kwargs):
        registration_code = kwargs["registration_code"]
        activation_success = User.activate_user(registration_code)
        context = super(ActivateAccount, self).get_context_data(**kwargs)
        context["activation_success"] = activation_success

        return context



# admin views
class LoadMatchesResults(UserPassesTestMixin, TemplateView):
    template_name = "bet/load_matches_results.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        try:
            python_path = settings.DATA_DOWNLOADER_PATH + "/venv/bin/python3.10"
            program_path = settings.DATA_DOWNLOADER_PATH + "/main.py"
            
            p = subprocess.Popen([python_path, program_path], cwd=settings.DATA_DOWNLOADER_PATH)

        except Exception as e:
            print(f"Command failed with return code {e}")

        return HttpResponse(f"Load Matches' Results. Check status in logs of program {settings.DATA_DOWNLOADER_PATH}")

class CalculatePredictionsPoints(UserPassesTestMixin, TemplateView):
    template_name = "bet/calculate_predictions_points.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        
        MatchPrediction.calculate_points()
        return super().get(request, *args, **kwargs)