from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

list_stat = ['pts', 'ast', 'stl', 'blk', 'tov', 'fgm2', 'fga2', 'fg2', 'fgm3', 'fga3', 'fg3',
             'fg', 'fgm', 'fga', 'fta', 'ftm', 'ft', 'reb', 'oreb', 'dreb', 'eff', 'plus_minus']
# Create your views here.
from django.views.generic import ListView

from statistic.models import Player, Game1, AverageStat, Game2,Game3, Game4

def show_main_page(request):
    best_scorer = AverageStat.objects.order_by('-pts')[0]
    best_blockshoter = AverageStat.objects.order_by('-blk')[0]
    best_rebounder = AverageStat.objects.order_by('-reb')[0]
    best_assister = AverageStat.objects.order_by('-ast')[0]
    best_stealer = AverageStat.objects.order_by('-stl')[0]
    context = {'best_scorer': best_scorer,
               'best_blockshoter':best_blockshoter,
               'best_rebounder': best_rebounder,
               'best_assister': best_assister,
               'best_stealer': best_stealer}
    return render(request, 'statistic/index.html', context=context)

def show_smth(request):
    lokomotiv = Player.objects.filter(team='1')
    bears = Player.objects.filter(team='2')
    oilers = Player.objects.filter(team='3')

    context = {'lokomotiv': lokomotiv,
               'bears': bears,
               'oilers': oilers}

    return render(request, 'statistic/Статистика-общая.html', context=context)
    # return HttpResponse("Страница")

def rating(player, stat):
    if stat == 'tov':
        for index, item in enumerate(AverageStat.objects.order_by('tov')):
            if item.name.name == str.capitalize(player):
                return index + 1
    else:
        for index,item in enumerate(AverageStat.objects.order_by(f'-{stat}')):
            if item.name.name == str.capitalize(player):
                return index + 1


def show_player(request, player_name):

    player = Player.objects.filter(name=str.capitalize(player_name)).first()
    stat = player.avg_stats.all()[0]
    game1_stat = Game1.objects.filter(name=str.capitalize(player_name)).first()
    game2_stat = Game2.objects.filter(name=str.capitalize(player_name)).first()
    game3_stat = Game3.objects.filter(name=str.capitalize(player_name)).first()
    game4_stat = Game4.objects.filter(name=str.capitalize(player_name)).first()
    avg_stat = AverageStat.objects.filter(name=str.capitalize(player_name)).first()
    rating_list = [rating('Gomov', i) for i in list_stat]
    context = {'player': player,
               'stat': stat,
               'game1_stat': game1_stat,
               'game2_stat': game2_stat,
               'game3_stat': game3_stat,
               'game4_stat': game4_stat,
               'avg_stat': avg_stat,
               'rating': rating_list}
    return render(request, 'statistic/Страница-игрока.html', context=context)

def show_team(request):
    return HttpResponse("Страница команды")

def pageNotFound(request, exception):
    return HttpResponseNotFound("Извините, но такой страницы не существует")

# class playerTest(ListView):
#     model = Player
#     template_name ='statistic/player.html'
#     context_object_name = 'player'
#
#     # def get_queryset(self):
#     #     return Player.objects.order_by('-stats1__pts')[:5]

# class playerTest(ListView):
#     model = Game1
#     template_name ='statistic/home.html'
#     context_object_name = 'players'
#
#
#     def get_queryset(self):
#         return AverageStat.objects.all().select_related('name').order_by('-min')[:5]
#
# def show_player(request, player_name):
#     player = get_object_or_404(Player, name=player_name)
#     context = {'player': player,
#                'title': player.name,
#                }
#     return render(request, 'statistic/home2.html', context=context)