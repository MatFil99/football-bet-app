from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


# Create your models here.
class FootballTeam(models.Model):
    football_team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, null=False, default=None)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # if self.name == "":
        #     raise Exception("FootballTeam with no name cannot be created!")

    class Meta:
        db_table = 'football_teams'


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
    season = models.CharField(max_length=9)
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    class Meta:
        db_table = 'matches'


class User(AbstractUser):
    # match_predictions = 


    class Meta:
        db_table = 'users'


class MatchPrediction(models.Model):
    match_prediction_id = models.AutoField(primary_key=True)
    match = models.ForeignKey(Match, null=False, on_delete=models.CASCADE, related_name="match_predictions", default=None)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="user_predictions", default=None)
    home_score_prediction = models.IntegerField(null=True)
    away_score_prediction = models.IntegerField(null=True)
    points = models.IntegerField(null=True)

    class Meta:
        db_table = 'match_predictions'
        unique_together = [['match_id', 'user_id']]


