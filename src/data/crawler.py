import logging
import os
import re
import pickle
from collections import defaultdict

import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.env import PROJECT_DIR, CP_DICT, HEADER

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)


class DaumNewsCrawler(object):
    def __init__(self, outlet, search_keyword):
        self.outlet = outlet
        self.output_dir = PROJECT_DIR / 'data' / 'raw' / self.outlet
        os.makedirs(self.output_dir, exist_ok=True)
        self._cp_key = CP_DICT[outlet]
        self.search_keyword = search_keyword
        self._data = defaultdict(list)

    def crawl(self, start_date, end_date, save_batch_size=100):
        """
        :param start_date: int of yyyymmdd for starting date
        :param end_date: int of yyyymmdd for end date
        :param save_batch_size: for every `save_batch_size` articles, save them..
        """

        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        logger.info(
            f"Crawling from {start_date} to {end_date} in {self.outlet}. "
            f"Saving every {save_batch_size} articles.")

        page_num = 1
        crawl = True
        num_total_results = None
        num_crawled = 0
        num_saved = 0
        cur_page_start = 1
        save_count = 0
        save_paths = []

        num_regex = re.compile(r'\d+')

        while crawl:
            url = f"https://search.daum.net/search?w=news" \
                  f"&q={self.search_keyword}" \
                  f"&cp={self._cp_key}" \
                  f"&p={page_num}" \
                  f"&DA=PGD&cluster=n" \
                  f"&sd={start_date}000000&ed={end_date}235959" \
                  f"&period=u"

            raw = requests.get(url, headers=HEADER)

            if raw.status_code != 200:
                logger.warning("404 at {url}")
                continue

            html = BeautifulSoup(raw.text, "html.parser")

            cnt_text = html.select_one("span#resultCntArea").text
            cur_page_range, cnt = cnt_text.split("/")

            if num_total_results is None:
                num_total_results = int(''.join(num_regex.findall(cnt)))
            else:
                cur_page_start = int(''.join(num_regex.findall(cur_page_range.split("-")[0])))

                if cur_page_start > num_total_results:
                    save_path = self._save(start_date, end_date, save_count=save_count)
                    save_paths.append(save_path)
                    logger.info(f"Crawled all ({num_crawled}) articles. Terminating...")
                    break

            articles = html.select("ul#newsResultUL > li")

            for i, ar in enumerate(articles):
                article_url = ar.select_one('a.f_nb')['href']
                article_res = requests.get(
                    article_url, headers=HEADER)

                if article_res.status_code != 200:
                    logger.debug(f"Could not get article {article_url}. Skipping...")
                    continue

                article_html = BeautifulSoup(article_res.text, "html.parser")

                title = article_html.select_one("h3.tit_view").text.strip()
                date = article_html.select_one("span.num_date").text.strip()
                summary_view = article_html.select_one("strong.summary_view")
                if summary_view is not None:
                    summary = summary_view.text.strip()
                else:
                    summary = None
                paragraphs = article_html.find_all(attrs={"dmcf-ptype": "general"})
                text = '\n\n'.join([p.text.strip() for p in paragraphs])

                if "기본소득" not in text and "기본 소득" not in text:
                    continue

                self._data['url'].append(article_url)
                self._data['title'].append(title)
                self._data['date'].append(date)
                self._data['summary'].append(summary)
                self._data['text'].append(text)
                num_crawled += 1

            logger.info(
                f"Crawled page {page_num:3d} "
                f"({num_crawled:4d} relevant articles out of {num_total_results} search results)")

            if num_saved + save_batch_size <= num_crawled or num_crawled >= num_total_results:
                logger.debug("Saving...")  # latter case: terminate
                save_path = self._save(start_date, end_date, save_count=save_count)
                save_paths.append(save_path)
                save_count += 1
                num_saved = num_crawled
                logger.debug(f"Saved {num_saved} results.")
                self._clean()

            page_num += 1

        # SAVE
        if num_crawled == 0:
            logger.info(f"No articles found during {start_date}-{end_date}")
            return None

        dfs = []

        logger.info("Combining all articles into a single csv file...")
        for path in save_paths:
            with open(path, "rb") as fp:
                _data = pickle.load(fp)
            dfs.append(pd.DataFrame(_data))
            os.remove(path)

        df = pd.concat(dfs)
        df = df[['date', 'url', 'title', 'summary', 'text']]
        csv_path = self.output_dir / f'{start_date}-{end_date}.csv'
        df.to_csv(csv_path, index=False)
        logger.info(f"Saved results to {csv_path}")

    def _save(self, start_date, end_date, save_count):
        save_path = self.output_dir / f'{start_date}-{end_date}_{save_count:03d}.pkl'

        with open(save_path, "wb") as fp:
            pickle.dump(self._data, fp)

        return save_path

    def _clean(self):
        self._data = defaultdict(list)
