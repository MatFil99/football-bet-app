from typing import Any
import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import Max, F, Q, Count, Min, Sum, Value, Prefetch, Subquery, OuterRef
from itertools import chain

import pytz
import random

from .services import send_activation_email
from .bet_rules import *

class CustomUserManager(BaseUserManager):
    ACTIVATION_EMAIL_SUBJECT = "Activation email BetApp"
    ACTIVATION_EMAIL_MESSAGE = "Use activation code below to finish registration on BetApp website."

    def create_user(self, username, password=None, **kwargs):
        """
        """
        email, first_name, last_name = "", "", ""
        if "email" in kwargs:
            email = kwargs["email"]
        if "first_name" in kwargs:
            first_name = kwargs["first_name"]
        if "last_name" in kwargs:
            last_name = kwargs["last_name"]

        code = self.generate_activation_code()

        if not password:
            raise ValueError("Cannot create User without password")
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            activation_code=code,
            is_active=False
        )
        user.set_password(password)
        user.save()
        self.send_activation_email(code, email)
        
        return user
    
    def generate_activation_code(self):
        code_number = random.randint(0, 10**User.ACTIVATION_CODE_LENGTH - 1)
        code = str(code_number).zfill(User.ACTIVATION_CODE_LENGTH)
        return code
    
    def send_activation_email(self, code, recipient):
        msg = CustomUserManager.ACTIVATION_EMAIL_MESSAGE + " Activation code: " + code
        send_activation_email(
            subject=CustomUserManager.ACTIVATION_EMAIL_SUBJECT,
            message=msg,
            recipient=recipient
            )


# Create your models here.
class FootballTeam(models.Model):
    football_team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, default=None)
    fullname = models.CharField(max_length=150, null=True, default=None)
    address = models.CharField(max_length=150, null=True, default=None)
    founded = models.DateField(null=True, default=None)
    website = models.CharField(max_length=50, null=True, default=None)
    league = models.CharField(max_length=25, null=True, default=None)
    

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # if self.name == "":
        #     raise Exception("FootballTeam with no name cannot be created!")

    class Meta:
        db_table = 'football_teams'

    def get_teams(league, season):
        # team_matches = FootballTeam.objects.filter(Q(league=league) & (Q(home_matches_season=season) | Q(away_matches__season=season)))
        team_matches = FootballTeam.objects.filter(league=league).filter(home_matches__season=season) | FootballTeam.objects.filter(league=league).filter(away_matches__season=season)
        return team_matches.distinct()

    def get_teams_stats(league, season):
        """
        """
        hmc = FootballTeam.objects.filter(Q(league=league) & Q(home_matches__season=season)).distinct() \
            .annotate(
                num_home_matches=Count("home_matches", filter=Q(home_matches__home_score__isnull=False)),
                home_scored_goals=Sum("home_matches__home_score", filter=Q(home_matches__home_score__isnull=False)),
                home_lost_goals=Sum("home_matches__away_score", filter=Q(home_matches__home_score__isnull=False)),
                home_win=Count("home_matches", filter=Q(home_matches__home_score__gt=F("home_matches__away_score"))),
                home_lost=Count("home_matches", filter=Q(home_matches__home_score__lt=F("home_matches__away_score"))),
                home_draw=Count("home_matches", filter=Q(home_matches__home_score=F("home_matches__away_score"))),
            )
            
        ft_stats = FootballTeam.objects.filter(Q(league=league) & Q(away_matches__season=season)).distinct() \
            .annotate(
                num_away_matches=Count("away_matches", filter=Q(away_matches__away_score__isnull=False)),
                away_scored_goals=Sum("away_matches__away_score", filter=Q(away_matches__away_score__isnull=False)),
                away_lost_goals=Sum("away_matches__home_score", filter=Q(away_matches__away_score__isnull=False)),
                away_win=Count("away_matches", filter=Q(away_matches__away_score__gt=F("away_matches__home_score"))),
                away_lost=Count("away_matches", filter=Q(away_matches__away_score__lt=F("away_matches__home_score"))),
                away_draw=Count("away_matches", filter=Q(away_matches__away_score=F("away_matches__home_score"))),

                num_home_matches=Subquery(hmc.filter(football_team_id=OuterRef("football_team_id")).values("num_home_matches")),
                home_scored_goals=Subquery(hmc.filter(football_team_id=OuterRef("football_team_id")).values("home_scored_goals")),
                home_lost_goals=Subquery(hmc.filter(football_team_id=OuterRef("football_team_id")).values("home_lost_goals")),
                home_win=Subquery(hmc.filter(football_team_id=OuterRef("football_team_id")).values("home_win")),
                home_lost=Subquery(hmc.filter(football_team_id=OuterRef("football_team_id")).values("home_lost")),
                home_draw=Subquery(hmc.filter(football_team_id=OuterRef("football_team_id")).values("home_draw")),
            )

        ft_stats = ft_stats \
            .annotate(
                total_matches=(F("num_home_matches")+F("num_away_matches")),
                total_win=(F("home_win")+F("away_win")),
                total_lost=(F("home_lost")+F("away_lost")),
                total_draw=(F("home_draw")+F("away_draw")),
                total_points=(3*(F("home_win")+F("away_win")) + F("home_draw")+F("away_draw")),
                total_scored_goals=(F("home_scored_goals")+F("away_scored_goals")),
                total_lost_goals=(F("home_lost_goals")+F("away_lost_goals")),
                goals_balance=(F("home_scored_goals")+F("away_scored_goals")-F("home_lost_goals")-F("away_lost_goals")),
            ) \
            .order_by("-total_points", "-goals_balance", "-total_scored_goals")

        # print(ft_stats.values().get(football_team_id=1))

        return ft_stats


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    # ?
    home_team = models.ForeignKey(FootballTeam, null=False, on_delete=models.CASCADE, related_name='home_matches', default=None)
    away_team = models.ForeignKey(FootballTeam, null=False, on_delete=models.CASCADE, related_name='away_matches', default=None)
    # home_team = models.ForeignKey(FootballTeam, null=True, on_delete=models.SET_NULL, related_name='home_matches')
    # away_team = models.ForeignKey(FootballTeam, null=True, on_delete=models.SET_NULL, related_name='away_matches')
    # ?
    matchday = models.IntegerField()
    date = models.DateTimeField(null=True)
    season = models.CharField(max_length=9, null=True)
    home_score = models.IntegerField(null=True)
    away_score = models.IntegerField(null=True)

    class Meta:
        db_table = 'matches'

    def get_current_season(league = None):
        if league:
            matches = Match.objects.filter(home_team__league=league) | Match.objects.filter(away_team__league=league)
        else:
            matches = Match.objects.all()
        
        season = matches.aggregate(Max("season"))
        season = None if season is None else season["season__max"]
        return season

    def get_current_matchday(league, season):
        if league is None or season is None:
            print("None values")
            return None
        
        matches = Match.objects.filter(home_team__league=league).filter(season=season) | Match.objects.filter(away_team__league=league).filter(season=season)
        ordered_matches = matches.filter(date__lte=datetime.datetime.now()).order_by("-date")
        no_matchday_matches = FootballTeam.get_teams(league=league, season=season).count()/2
        matchday = ordered_matches[int((no_matchday_matches+1)/2)].matchday
        return matchday

    def match_played_or_started(self):
        return datetime.datetime.now() >= self.date

class User(AbstractUser):

    objects = CustomUserManager()
    activation_code = models.CharField(max_length=6, null=True)
    ACTIVATION_CODE_LENGTH = 6

    class Meta:
        db_table = 'users'

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # if "password" not in kwargs or kwargs["password"] in [None, ""]:
        #     raise Exception("Cannot create user without password")
        super().__init__(*args, **kwargs)

    def activate_user(registration_code: str):
        """
        """
        try:
            user = User.objects.get(activation_code=registration_code)
            user.is_active = True
            user.activation_code = None
            user.save()
            return True
        except:
            return False

class MatchComment(models.Model):

    match = models.ForeignKey(Match, null=False, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    author = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)

    class Meta:
        db_table = "match_comments"

    def get_match_comments(match_id):
        return MatchComment.objects.filter(match_id=match_id).order_by("date")

    def create(match, author, text):
        date = datetime.datetime.now()
        comment = MatchComment(
            author=author,
            match=match,
            text=text,
            date=date,
            )
        
        comment.save()
        return comment



class MatchPrediction(models.Model):
    match_prediction_id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, null=False, on_delete=models.CASCADE, related_name="match_predictions", default=None)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="user_predictions", default=None)
    home_score_prediction = models.IntegerField(null=True)
    away_score_prediction = models.IntegerField(null=True)
    points = models.IntegerField(null=True)


    def __init__(self, *args, **kwargs):
        self.bet_rules = [ExactResultRule(2,0), GeneralResultRule(1,0)]
        super().__init__(*args, **kwargs)
    

    class Meta:
        db_table = 'match_predictions'
        unique_together = [['match_id', 'user_id']]

    def get_user_match_prediction(user, match):
        mp = None
        try:
            mp = MatchPrediction.objects.get(match=match, user=user)
        except Exception as e:
            print(e)
        return mp

    def get_ranking():
        ranking = User.objects \
            .filter(Q(is_staff=False) & Q(is_superuser=False)) \
            .annotate(points=Sum("user_predictions__points")) \
            .order_by(F("points").desc(nulls_last=True))
        
        return ranking

    def update_prediction(self, home_score, away_score):
        self.home_score_prediction = home_score
        self.away_score_prediction = away_score
        self.save()

    def calculate_points():
        """
        """
        match_predictions = MatchPrediction.objects.filter(
            Q(match__home_score__isnull=False)
            & Q(points__isnull=True)
        )

        for prediction in match_predictions:
            prediction_info = {
                "home_score": prediction.home_score_prediction,
                "away_score": prediction.away_score_prediction,
            }
            match_info = {
                "home_score": prediction.match.home_score,
                "away_score": prediction.match.away_score,
            }
            
            points = 0 
            for rule in prediction.bet_rules:
                points += rule.score(prediction_info, match_info)

            prediction.points = points
            prediction.save()

