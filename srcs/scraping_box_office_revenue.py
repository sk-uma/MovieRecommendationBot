import requests
from bs4 import BeautifulSoup
import io
import datetime
import pandas as pd

URL = 'https://mimorin2014.blog.fc2.com/blog-date-\
                    {year:4d}{month:2d}{date:2d}.html'


def get_dateURL(year, month, date):
    return URL.format(year=year, month=month, date=date)


def get_ranking(year, month, date):
    res = requests.get(get_dateURL(year, month, date))
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
            return df


def get_latest_ranking():
    now = datetime.datetime.now()
    return get_ranking(now.year, now.month, now.day - 1)
