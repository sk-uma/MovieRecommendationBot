import requests
import json
from pprint import pprint
import os
from dotenv import dotenv_values
import random

temp = dotenv_values(".env")
TOKEN = temp["TMDB_APIKEY"]

random.seed(42)


class TMDB:
    def __init__(self, token):
        self.token = token
        self.headers_ = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json;charset=utf-8'
        }
        self.base_url_ = 'https://api.themoviedb.org/3/'
        self.img_base_url_ = 'https://image.tmdb.org/t/p/w500'

    def _json_by_get_request(self, url, params={}):
        res = requests.get(url, headers=self.headers_, params=params)
        return json.loads(res.text)

    def search_movies(self, query, page=1):
        params = {
            'query': query,
            'language': 'ja',
            'page': page,
            'include_adult': False
        }
        url = f'{self.base_url_}search/movie'
        return self._json_by_get_request(url, params)

    def search_person(self, query):
        params = {'query': query, 'language': 'ja', 'include_adult': False}
        url = f'{self.base_url_}search/person'
        return self._json_by_get_request(url, params)

    def get_movies_for_cast_and_category(self, cast_id_list,
                                         category_id, page=1):
        params = {
            'with_genres': category_id,
            'with_people': ",".join(cast_id_list),
            'sort_by': 'popularity.desc',
            'language': 'ja',
            'include_adult': False
        }
        url = f'{self.base_url_}discover/movie'
        return self._json_by_get_request(url, params)

    def get_movie_images(self, movie_id, language=None):
        params = {'include_adult': False}
        url = f'{self.base_url_}movie/{movie_id}/images'
        return self._json_by_get_request(url, params)

    def get_popular_movies(self, page=1):
        params = {'language': 'ja', 'include_adult': False}
        url = f'{self.base_url_}movie/popular'
        return self._json_by_get_request(url, params)

    def get_movie(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}'
        return self._json_by_get_request(url)

    def get_movie_account_states(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/account_states'
        return self._json_by_get_request(url)

    def get_movie_alternative_titles(self, movie_id, country=None):
        url = f'{self.base_url_}movie/{movie_id}/alternative_titles'
        return self._json_by_get_request(url)

    def get_movie_changes(self, movie_id, start_date=None, end_date=None):
        url = f'{self.base_url_}movie/{movie_id}'
        return self._json_by_get_request(url)

    def get_movie_credits(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/credits'
        return self._json_by_get_request(url)

    def get_movie_external_ids(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/external_ids'
        return self._json_by_get_request(url)

    def get_movie_keywords(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/keywords'
        return self._json_by_get_request(url)

    def get_movie_release_dates(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/release_dates'
        return self._json_by_get_request(url)

    def get_movie_videos(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/videos'
        return self._json_by_get_request(url)

    def get_movie_translations(self, movie_id):
        url = f'{self.base_url_}movie/{movie_id}/translations'
        return self._json_by_get_request(url)

    def get_movie_recommendations(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/recommendations'
        return self._json_by_get_request(url)

    def get_similar_movies(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/similar'
        return self._json_by_get_request(url)

    def get_movie_reviews(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/reviews'
        return self._json_by_get_request(url)

    def get_movie_lists(self, movie_id, language=None):
        url = f'{self.base_url_}movie/{movie_id}/lists'
        return self._json_by_get_request(url)

    def get_latest_movies(self, language=None):
        url = f'{self.base_url_}movie/latest'
        return self._json_by_get_request(url)

    def get_now_playing_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/now_playing'
        return self._json_by_get_request(url)

    def get_top_rated_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/top_rated'
        return self._json_by_get_request(url)

    def get_upcoming_movies(self, language=None, region=None):
        url = f'{self.base_url_}movie/upcoming'
        return self._json_by_get_request(url)


api = TMDB(TOKEN)


def get_cast_id_list(cast_list):
    cast_id_list = []
    without_cast = []
    cast = []
    for c in cast_list:
        res = api.search_person(c)
        if len(res['results']) > 0:
            cast_id_list.append(str(res['results'][0]['id']))
            cast.append(c)
        else:
            without_cast.append(cast)
    return cast_id_list, cast, without_cast


def get_movies_for_castname_and_category(cast_id_list, category, n=10):
    if category is not None:
        movies = api.get_movies_for_cast_and_category(cast_id_list,
                                                      category['id'])
    else:
        movies = api.get_movies_for_cast_and_category(cast_id_list, "")
    for page in list(range(2, movies['total_pages'] + 1))[:n-1]:
        res = api.get_movies_for_cast_and_category(cast_id_list,
                                                   category['id'],
                                                   page=page)
        movies['results'] = movies['results'] + res['results']
    return movies['results']


def get_movies_for_query(query, n=10):
    movies = api.search_movies(query)
    for page in list(range(2, movies['total_pages'] + 1))[:n - 1]:
        res = api.search_movies(query, page=page)
        movies['results'] = movies['results'] + res['results']
    return movies['results']


def get_popular_movies(n=10):
    movies = api.get_popular_movies()
    for page in list(range(2, movies['total_pages'] + 1))[:n - 1]:
        res = api.get_popular_movies(page=page)
        movies['results'] = movies['results'] + res['results']
    return movies['results']


def get_poster_url(movie):
    image = api.get_movie_images(movie['id'])
    if len(image['posters']) == 0:
        return None
    return api.img_base_url_ + image['posters'][0]['file_path']


def get_movies(cast_list, info, category):
    cast_id_list, cast, without_cast = get_cast_id_list(cast_list)
    movies = []
    if len(cast) != 0:
        movies = get_movies_for_castname_and_category(cast_id_list, category)
        movies = random.sample(movies, min(3, len(movies)))
    if len(movies) == 0 and len(without_cast) != 0:
        for wc in without_cast:
            movies = movies + get_movies_for_query(wc, n=1)
        movies = random.sample(movies, min(3, len(movies)))
    if len(movies) == 0 and len(info) != 0 and category is not None:
        for i in info:
            movies = movies + get_movies_for_query(i, n=1)
        movies = random.sample(movies, min(1, len(movies)))
        category_movies = get_movies_for_castname_and_category([], category)
        movies = movies + random.sample(category_movies,
                                        min(3 - len(movies),
                                            len(category_movies)))
    if len(movies) == 0 and len(info) != 0:
        for i in info:
            movies = movies + get_movies_for_query(i, n=1)[:5]
        movies = random.sample(movies, min(3, len(movies)))
    if len(movies) == 0 and category is not None:
        movies = get_movies_for_castname_and_category([], category)
        movies = random.sample(movies, min(3, len(movies)))
    if len(movies) == 0:
        movies = get_popular_movies(n=5)
        movies = random.sample(movies, min(3, len(movies)))
    return movies


def get_movie(word):
    words = []
    api = TMDB(TOKEN)
    res = api.search_movies(word)

    for i in range(res['total_results']):
        movie_title = res['results'][i]['original_title']
        words.append(movie_title)

    return words


def display(movies):
    print()
    for movie in movies:
        print(movie['title'])


if __name__ == '__main__':
    display(get_movies([], ['サイエンスフィクション'],
                       {'id': 878, 'name': 'サイエンスフィクション'}))
    display(get_movies([], ['西部劇'], {'id': 37, 'name': '西部劇'}))
    display(get_movies([], ['SF'], {'id': 878, 'name': 'サイエンスフィクション'}))
    display(get_movies([], ['怖い'], {'id': 27, 'name': 'ホラー'}))
    display(get_movies([], ['マーベル'], {'id': 27, 'name': 'ホラー'}))
    display(get_movies(['木村拓哉'], [], None))
    display(get_movies(['木村拓哉'], ['サスペンス映画'], {'id': 53, 'name': 'スリラー'}))
    display(get_movies([], ['ウィル・スミス'], {'id': 10751, 'name': 'ファミリー映画'}))
    display(get_movies(['トム'], ['クルーズ'], {'id': 12, 'name': 'アドベンチャー'}))
    display(get_movies(['山本美月', '甲本雅裕'], ['怖い'], {'id': 27, 'name': 'ホラー'}))
    display(get_movies([], ['ドラえもん'], None))
    display(get_movies([], ['人気'], {'id': 35, 'name': 'コメディ'}))
