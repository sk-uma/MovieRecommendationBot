import requests
from bs4 import BeautifulSoup
import io
import datetime
import pandas as pd
from get_movie import get_movies_for_query, get_poster_url

DATAFILE_PATH = '/root/chatBot/csv_data/ranking.csv'
URL = 'https://mimorin2014.blog.fc2.com/blog-date-\
                    {year:4d}{month:2d}{day:2d}.html'


def get_dateURL(year, month, day):
    return URL.format(year=year, month=month, day=day)


def scraping_ranking(year, month, day):
    res = requests.get(get_dateURL(year, month, day))
    soup = BeautifulSoup(res.text, 'html.parser')
    tags = soup.find_all(class_="content entry grid_content")
    for tag in tags:
        if 'id' in tag.attrs.keys():
            entry_body = tag.find(class_="entry_body")
            entry_body.p.decompose()
            parse_text = str(entry_body).replace('<br/>', '\n')
            parse_text = parse_text.replace('*', '')
            parse_text = parse_text.replace('　', ',').splitlines()[3:-2]
            df = pd.read_csv(io.StringIO('\n'.join(parse_text)), header=None,
                             usecols=[0, 6], names=['rank', 'title'])
            df = df.set_index('rank')
            return df
    return None


def scraping_latest_ranking():
    now = datetime.datetime.now()
    return scraping_ranking(now.year, now.month, now.day - 1)


def reload_ranking_csv():
    df = scraping_latest_ranking()
    new_df = pd.DataFrame(columns=['title', 'rank', 'URL'])
    new_df = new_df.set_index('rank')
    for _, row in df.iterrows():
        movies = get_movies_for_query(row['title'], n=1)
        if len(movies) != 0:
            movie = movies[0]
            poster_url = get_poster_url(movie)
            new_df = new_df.append({
                'title': movie['title'],
                'URL': poster_url
            }, ignore_index=True)
        if new_df.shape[0] >= 3:
            break
    csv_text = new_df.to_csv()
    with open(DATAFILE_PATH, 'w') as f:
        f.write(csv_text)


if __name__ == '__main__':
    reload_ranking_csv()
