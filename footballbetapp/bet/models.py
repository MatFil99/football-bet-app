from typing import Any
from django.db import models



# Create your models here.
class FootballTeam(models.Model):
    football_team_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.name == "":
            raise Exception("FootballTeam with no name cannot be created!")

    class Meta:
        db_table = 'football_teams'


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    home_team_id = models.ForeignKey(FootballTeam, null=True, on_delete=models.SET_NULL, related_name='home_matches')
    away_team_id = models.ForeignKey(FootballTeam, null=True, on_delete=models.SET_NULL, related_name='away_matches')
    matchday = models.IntegerField()
    date = models.DateTimeField(null=True)
    season = models.CharField(max_length=9)
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    class Meta:
        db_table = 'matches'


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(null=True, max_length=30)
    surname = models.CharField(null=True, max_length=30)
    pass_hash = models.CharField(null=True, max_length=100)
    username = models.CharField(null=True, max_length=20)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = 'users'


class MatchPrediction(models.Model):
    # prediction_id = models.AutoField(primary_key=True)
    match_id = models.ForeignKey(Match, null=True, on_delete=models.SET_NULL, db_column='match_id')
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, db_column='user_id')
    home_score_prediction = models.IntegerField(null=True)
    away_score_prediction = models.IntegerField(null=True)
    points = models.IntegerField(null=True)

    class Meta:
        db_table = 'match_predictions'
        unique_together = [['match_id', 'user_id']]



# class ModelPrefix:

#     def __init__(self) -> None:
#         pass




# example of metaclass usage to set prefix for every Model class that inherit specific class
# class MyModelBase( ModelBase ):
#     def __new__( cls, name, bases, attrs, **kwargs ):
#         if name != "MyModel":
#             class MetaB:
#                 db_table = "FOO_" + name

#             attrs["Meta"] = MetaB

#         r = super().__new__( cls, name, bases, attrs, **kwargs )
#         return r       

# class MyModel( Model, metaclass = MyModelBase ):
#     class Meta:
#         abstract = True

# class Businesses( MyModel ):
#     ...