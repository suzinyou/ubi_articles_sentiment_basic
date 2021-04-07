from src.data.crawler import DaumNewsCrawler
from src.env import KEYWORD, CP_DICT, DATE_RANGES

if __name__ == "__main__":
    for outlet in CP_DICT.keys():
        crawler = DaumNewsCrawler(outlet=outlet, search_keyword=KEYWORD)

        for sd, ed in DATE_RANGES:
            crawler.crawl(start_date=sd, end_date=ed,)