import functools
import json
import time
import re

import requests
from bs4 import BeautifulSoup, SoupStrainer
from django.core.management.base import BaseCommand

from tvcrawler.models import Movie

excluded = re.compile(r'中国电影报道|光影星播客|音乐电影欣赏.*|今日影评|国片大首映.*')
remove_unnecessary = functools.partial(re.compile(r'（[上中下]）').sub, '')


def get(url):
    time.sleep(3)
    r = requests.get(url)
    while r.status_code == 400:
        print('Got http 400, sleep 10min...')
        time.sleep(600)
        r = requests.get(url)
    return r


def get_movie_info(name):
    name = remove_unnecessary(name)
    r = get('https://api.douban.com/v2/movie/search?count=1&q=' + name)
    info = json.loads(r.text)['subjects']
    if len(info) == 0:
        return None
    info = info[0]
    if info['title'] != name:  # FIXME
        return None
    return info


def get_movie_summary(id):
    r = get('https://api.douban.com/v2/movie/' + id)
    summary = json.loads(r.text)['summary']
    if len(summary) > 300:
        summary = summary[:300] + '……'
    return summary


def save_movies(channel):
    r = requests.get('http://hdtv.neu6.edu.cn/time-select?p=' + channel)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml', parse_only=SoupStrainer('div'))
    for div in soup.find_all(id='list_item'):
        next = div.find_next()
        if next['id'] != 'list_status':
            continue
        movie_name = div.text[6:]
        if excluded.match(movie_name):
            print('excluded:', movie_name)
            continue
        a, *_ = next.children
        if a.text == '直播中':
            print('live ignored:', movie_name)
            continue
        timeline = a['href'][23:]
        movie_len = -eval(timeline[:-len(channel) - 1])
        if movie_len < 12 * 60:
            print('short movie ignored:', movie_name, movie_len / 60, 'min')
            continue
        info = get_movie_info(movie_name)
        if info is None:
            print('not in douban:', movie_name)
            continue
        if info['rating']['average'] < 7:
            print('low rating ignored:', movie_name, info['rating']['average'])
            continue

        Movie(
            title=movie_name,
            rating=info['rating']['average'],
            genres=' / '.join(info['genres']),
            summary=get_movie_summary(info['id']),
            movie_id=info['id'],
            timeline=timeline,
            image=info['images']['large']
        ).save()
        print('[SAVED]', movie_name)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Movie.objects.all().delete()
        save_movies('chchd')
        print('\n[DONE] chcd')
        save_movies('chcatv')
        print('\n[DONE] chcatv')
        save_movies('cctv6hd')
        print('\n[DONE] cctv6hd')
        print('\nAll done.')
