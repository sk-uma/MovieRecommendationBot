import requests
import json


DATAFILE_PATH = '../json_data/ranking.json'

def get_ranking():
    with open(DATAFILE_PATH, 'r') as f:
        json_text = f.read()
    json_data = json.loads(json_text)
    return json_data


if __name__ == '__main__':
    print(get_ranking())
