from django.shortcuts import render

from .models import Movie


def index(request):
    movies = Movie.objects.all()
    return render(request, 'tvcrawler/index.html', {'movies': movies})


def play(request, timeline):
    context = {
        'play_link': 'http://tv.udoubi.top/media2/program-{}.m3u8'.format(timeline)
    }
    return render(request, 'tvcrawler/player.html', context)
