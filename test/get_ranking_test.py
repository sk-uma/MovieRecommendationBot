import sys
sys.path.append('../')
from srcs.scraping_box_office_revenue import get_latest_ranking

if __name__ == '__main__':
    print(get_latest_ranking())
