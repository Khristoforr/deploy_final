from django.contrib import admin
from .models import *
# Register your models here.

def change_team_bears(modeladmin, request, queryset):
    queryset.update(team=2)

def change_team_loko(modeladmin, request, queryset):
        queryset.update(team=1)


def change_team_oilers(modeladmin, request, queryset):
    queryset.update(team=3)

class AwardsInline(admin.TabularInline):
    model = Awards
    extra = 3

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'rus_first_name', 'rus_last_name', 'photo')
    list_editable = ('team', 'rus_first_name', 'rus_last_name', 'photo' )
    actions = [change_team_bears, change_team_loko, change_team_oilers]
    inlines = [AwardsInline,]
admin.site.register(Player, PlayerAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'wins', 'losses', 'image')
    list_editable = ('wins', 'losses', 'image')
admin.site.register(Team, TeamAdmin)

class AwardsAdmin(admin.ModelAdmin):
    list_display = ('achievement','get_player', 'player', 'year_awarded')
    list_editable = ('player','year_awarded')

    def get_player(self,obj):
        return obj.player.team

admin.site.register(Awards, AwardsAdmin)

class AverageStatAdmin(admin.ModelAdmin):
    list_display = ('name',  'get_player', 'pts')
    list_editable = ('pts',)

    def get_player(self,obj):
        return obj

admin.site.register(Game1, AverageStatAdmin)

class AchievementsAdmin(admin.ModelAdmin):
    list_display = ('title',)
admin.site.register(Achievements, AchievementsAdmin)

class FileAdmin(admin.ModelAdmin):
    list_display = ('file',)

admin.site.register(Router)
