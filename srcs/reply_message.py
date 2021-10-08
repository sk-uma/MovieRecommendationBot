from parse_message import parse_message
from get_movie import get_movies, get_poster_url
import pandas as pd
import numpy as np

DATAFILE_PATH = '/root/chatBot/csv_data/ranking.csv'


def display_movie(title, url, update):
    print("in display_movie:", title, url)
    update.message.reply_text(title)
    print("in display_movie:", title, url, url is not np.nan, url is not None)
    if url is not np.nan and url is not None:
        update.message.reply_photo(url)


def display_ranking(update):
    df = pd.read_csv(DATAFILE_PATH)
    if df.shape[0] == 0:
        return False
    for _, row in df.iterrows():
        movie_title = row['title']
        poster_url = row['URL']
        display_movie(movie_title, poster_url, update)
    return True


def display_movies(movies, update):
    print(len(movies))
    for movie in movies:
        poster_url = get_poster_url(movie)
        print("in display_movies:", movie['title'], poster_url)
        display_movie(movie['title'], poster_url, update)


def reply_message(message, update):
    cast_list, info, category = parse_message(message)
    flag = False
    if '人気' in info:
        flag = display_ranking(update)
    if '人気' not in info or not flag:
        movies = get_movies(cast_list, info, category)
        display_movies(movies, update)
