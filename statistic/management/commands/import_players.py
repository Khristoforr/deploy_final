import xlrd
from django.core.management.base import BaseCommand
from statistic.models import Player

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def calculate_fg(self, fgm, fga):
        if int(fga) == 0:
            return 0
        else:
            return (int(fgm)/int(fga)) * 100

    def handle(self, *args, **options):
        workbook = xlrd.open_workbook('Players_info.xlsx', on_demand=True).sheet_by_index(0)
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
            Player.objects.create(name=player['name'],
                                  rus_first_name=player['rus_first_name'],
                                  rus_last_name=player['rus_last_name'],
                                  weight=player['weight'],
                                  age=player['age'],
                                  position=player['position'],
                                  height=player['height']
                                  )

