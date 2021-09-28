import sys
sys.path.append('../')
from srcs.scraping_box_office_revenue import scraping_latest_ranking

if __name__ == '__main__':
    print(scraping_latest_ranking())
