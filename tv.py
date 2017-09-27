from flask import Flask, render_template
from collections import namedtuple
import pickle


MovieInfo = namedtuple('MovieInfo', 'title rating genres summary id timeline image')

app = Flask(__name__)
with open('movies', 'rb') as f:
    movies = pickle.load(f)


@app.route('/')
def index():
    return render_template('index.html', movies=movies)


@app.route('/play/<timeline>/')
def play(timeline):
    return render_template('player.html', play_link='http://tv.udoubi.top/media2/program-{}.m3u8'.format(timeline))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
