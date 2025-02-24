from django.contrib import admin

from .models import FootballTeam, Match, User, MatchComment, MatchPrediction

# Register your models here.

class FootballTeamAdmin(admin.ModelAdmin):
    pass
    fields = ["name"]


admin.site.register(FootballTeam, FootballTeamAdmin)
admin.site.register(Match)
admin.site.register(User)
admin.site.register(MatchComment)
admin.site.register(MatchPrediction)