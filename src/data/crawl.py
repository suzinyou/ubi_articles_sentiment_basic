from src.data.crawler import DaumNewsCrawler
from src.env import KEYWORD, CP_DICT

if __name__ == "__main__":
    date_ranges = [
        ('20170101', '20200731'),
        # ('20170101', '20181231'),
        # ('20160101', '20181231'),
        # ('20130101', '20161231'),
        # ('20060101', '20121231'),
        # ('20000101', '20061231'),
        # ('19900101', '19991213')
    ]

    for outlet in CP_DICT.keys():
        crawler = DaumNewsCrawler(outlet=outlet, search_keyword=KEYWORD)

        for sd, ed in date_ranges:
            crawler.crawl(start_date=sd, end_date=ed, )