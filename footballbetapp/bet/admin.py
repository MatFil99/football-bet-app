from django.contrib import admin

from .models import FootballTeam, Match

# Register your models here.

class FootballTeamAdmin(admin.ModelAdmin):
    pass
    fields = ["name"]


admin.site.register(FootballTeam, FootballTeamAdmin)
admin.site.register(Match)