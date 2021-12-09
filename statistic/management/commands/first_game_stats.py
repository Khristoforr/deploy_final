import os

import xlrd
from django.core.management.base import BaseCommand
from statistic.models import Player, AverageStat, Game1, Game2, Game3, Game4


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def calculate_fg(self, fgm, fga):
        if int(fga) == 0:
            return 0
        else:
            return (int(fgm)/int(fga)) * 100

    def handle(self, *args, **options):
        AverageStat.objects.all().delete()
        game_list = [Game1, Game2, Game3, Game4]
        workbook = xlrd.open_workbook('media/files_2_upload/import_stats.xlsx', on_demand=True).sheet_by_index(0)
        first_row = []
        for col in range(workbook.ncols):
            first_row.append(workbook.cell_value(0, col))
        data = []
        for row in range(1, workbook.nrows):
            elm = {}
            for col in range(workbook.ncols):
                elm[first_row[col]] = workbook.cell_value(row, col)
            data.append(elm)

        for player in data:
            print(player['Player'])
            game_index = Player.objects.filter(name=player['Player']).first().games_played
            some_player = game_list[game_index](name_id=Player.objects.filter(name=player['Player'])[0].name,
                                 min=int((player['MIN'])[:1]),
                                 pts=player['PTS'],
                                 fgm2=player['2PM'],
                                 fga2=player['2PA'],
                                 fg2=self.calculate_fg(player['2PM'],player['2PA']),
                                 fgm3=player['3PM'],
                                 fga3=player['3PA'],
                                 fg3=self.calculate_fg(player['3PM'],player['3PA']),
                                 fgm=player['FGM'],
                                 fga=player['FGA'],
                                 fg=self.calculate_fg(player['FGM'],player['FGA']),
                                 ftm=player['FTM'],
                                 fta=player['FTA'],
                                 ft=self.calculate_fg(player['FTM'],player['FTA']),
                                 oreb=player['OREB'],
                                 dreb=player['DREB'],
                                 reb=player['REB'],
                                 ast=player['AST'],
                                 tov=player['TOV'],
                                 stl=player['STL'],
                                 blk=player['BLK'],
                                 eff=player['EFF'],
                                 plus_minus=player['+/-'],
                                     )
            Player.objects.filter(name=player['Player']).update(games_played=game_index + 1)
            some_player.save()

        for player in data:
            games_played = Player.objects.filter(name=player['Player'])[0].games_played
            some_player = AverageStat(name_id=Player.objects.filter(name=player['Player'])[0].name,
                                 min=sum([i.objects.filter(name=player['Player'])[0].min for i in game_list[0:games_played]])/games_played,
                                 pts=sum([i.objects.filter(name=player['Player'])[0].pts for i in game_list[0:games_played]])/games_played,
                                 fgm2=sum([i.objects.filter(name=player['Player'])[0].fgm2 for i in game_list[0:games_played]])/games_played,
                                 fga2=sum([i.objects.filter(name=player['Player'])[0].fga2 for i in game_list[0:games_played]])/games_played,
                                 fg2=sum([i.objects.filter(name=player['Player'])[0].fg2 for i in game_list[0:games_played]])/games_played,
                                 fgm3=sum([i.objects.filter(name=player['Player'])[0].fgm3 for i in game_list[0:games_played]])/games_played,
                                 fga3=sum([i.objects.filter(name=player['Player'])[0].fga3 for i in game_list[0:games_played]])/games_played,
                                 fg3=sum([i.objects.filter(name=player['Player'])[0].fg3 for i in game_list[0:games_played]])/games_played,
                                 fgm=sum([i.objects.filter(name=player['Player'])[0].fgm for i in game_list[0:games_played]])/games_played,
                                 fga=sum([i.objects.filter(name=player['Player'])[0].fga for i in game_list[0:games_played]])/games_played,
                                 fg=sum([i.objects.filter(name=player['Player'])[0].fg for i in game_list[0:games_played]])/games_played,
                                 ftm=sum([i.objects.filter(name=player['Player'])[0].ftm for i in game_list[0:games_played]])/games_played,
                                 fta=sum([i.objects.filter(name=player['Player'])[0].fta for i in game_list[0:games_played]])/games_played,
                                 ft=sum([i.objects.filter(name=player['Player'])[0].ft for i in game_list[0:games_played]])/games_played,
                                 oreb=sum([i.objects.filter(name=player['Player'])[0].oreb for i in game_list[0:games_played]])/games_played,
                                 dreb=sum([i.objects.filter(name=player['Player'])[0].dreb for i in game_list[0:games_played]])/games_played,
                                 reb=sum([i.objects.filter(name=player['Player'])[0].reb for i in game_list[0:games_played]])/games_played,
                                 ast=sum([i.objects.filter(name=player['Player'])[0].ast for i in game_list[0:games_played]])/games_played,
                                 tov=sum([i.objects.filter(name=player['Player'])[0].tov for i in game_list[0:games_played]])/games_played,
                                 stl=sum([i.objects.filter(name=player['Player'])[0].stl for i in game_list[0:games_played]])/games_played,
                                 blk=sum([i.objects.filter(name=player['Player'])[0].blk for i in game_list[0:games_played]])/games_played,
                                 eff=sum([i.objects.filter(name=player['Player'])[0].eff for i in game_list[0:games_played]])/games_played,
                                 plus_minus=sum([i.objects.filter(name=player['Player'])[0].plus_minus for i in game_list[0:games_played]])/games_played,
                                     )
            some_player.save()

        print("Экспорт данных выполнен успешно")
        os.remove('media/files_2_upload/import_stats.xlsx')