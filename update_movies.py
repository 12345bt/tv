import re
import time
import json
import pickle
import requests
from bs4 import BeautifulSoup, SoupStrainer
#  from collections import namedtuple


#  MovieInfo = namedtuple('MovieInfo', 'title rating genres summary id timeline image')
from tv import MovieInfo

excluded = re.compile(r'中国电影报道|光影星播客|音乐电影欣赏.*|今日影评|国片大首映.*')


def url_to_json(url):
    time.sleep(2)
    r = requests.get(url)
    while r.status_code == 400:
        print('Got 400 client error, sleep 5min...')
        time.sleep(300)
        r = requests.get(url)
    return json.loads(r.text)


def query_movie_info(name):
    print(name)
    movie = url_to_json('http://api.douban.com/v2/movie/search?count=1&q=' + name)['subjects']
    if len(movie) == 0:
        return None
    movie = movie[0]
    if movie['title'] != name:  # FIXME
        return None
    return MovieInfo(
        movie['title'], movie['rating']['average'], ' / '.join(movie['genres']),
        None, movie['id'], None, movie['images']['large'] 
    )


def get_movies(channel):
    #  r = requests.get('http://hdtv.neu6.edu.cn/time-select?p=' + channel)
    #  r.raise_for_status()
    with open('/home/csm/t') as f:
        text = f.read()
    soup = BeautifulSoup(text, 'lxml', parse_only=SoupStrainer('div'))
    for div in soup.find_all(id='list_item'):
        next = div.find_next()
        if next['id'] != 'list_status':
            continue
        movie_name = div.text[6:]
        if excluded.match(movie_name):
            continue
        a, *_ = next.children
        if a.text == '直播中':
            print('ignore live:', movie_name)
            continue
        timeline = a['href'][23:]
        movie_len = -eval(timeline[:-len(channel)-1])
        if movie_len < 12 * 60:
            print('ignore short movie:', movie_name, movie_len / 60, 'min')
            continue

        info = query_movie_info(movie_name)
        if info is None or info.rating < 7:
            continue

        summary = url_to_json('http://api.douban.com/v2/movie/' + info.id)['summary']
        if len(summary) > 200:
            summary = summary[:200] + '……'
        info = info._replace(timeline=timeline, summary=summary)
        yield info


if __name__ == '__main__':
    try:
        movies = []
        gen = get_movies('cctv6hd')
        while True:
            movies.append(next(gen))
    finally:
        with open('movies', 'wb') as f:
            pickle.dump(movies, f)
