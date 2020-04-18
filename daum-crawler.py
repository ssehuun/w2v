#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import argparse
import logging
import queue
import os
import sys
import threading
import time
import re
import requests
from bs4 import BeautifulSoup
import json
import config_load
import global_value
from utils import date_range, log, mysql

class News(object):
    def __init__(self, id, date, category):
        self.id = id
        self.date = date
        self.category = category

class Crawler():

    def __init__(self, mysql_db):
        self.mysql_db = mysql_db

    def crawl(self):
        days = date_range.getTimeTuple(global_value.START_DATE, global_value.END_DATE, 'D')
        for day in days:
            date = time.strftime('%Y%m%d', day)
            logging.info("Crawling links - " + date)
            title_list = []
            for category in global_value.CATEGORY_LIST:
                logging.info("Crawling links - " + category)
                for i in range(1, 1000):
                    url = global_value.BASE_LINKS_URL + category + "?regDate=" + date + "&page=" + str(i)
                    try:
                        req = requests.get(url)
                        html = req.text
                        soup = BeautifulSoup(html, 'html.parser')
                        none = soup.findAll('p', attrs={'class': 'txt_none'})
                        if len(none) > 0:
                            logging.debug("has no content: " + url)
                            break
                        else:
                            box = soup.find('ul', attrs={'class': 'list_allnews'})
                            links = box.findAll('a', attrs={'class': 'link_txt'})
                            for link in links:
                                title = link.text
                                if not self.check_title(title):
                                    continue
                                # 같은날짜 중복제목제거
                                if title in title_list:
                                    continue
                                title_list.append(title)
                                id = link['href'][-17:]
                                self.crawl_news(id, link['href'], category, date)
                    except Exception as e:
                        logging.error(url, e)
                        break

                time.sleep(global_value.CRAWL_LONG_INTERVAL)

    def crawl_news(self, id, link, category, date):

        url = global_value.BASE_NEWS_URL + id
        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')

        title_txt = soup.find('h3', attrs={'class': 'tit_view'}).text
        content = soup.find('div', attrs={'class': 'article_view'})

        has_vod = '0'
        if content.find('div', attrs={'class': 'video_frm'}) is not None:
            has_vod = '1'

        source = soup.find('meta', attrs={'name': 'article:media_name'})
        source_txt = source.get('content').strip()

        phases = content.findAll('p')
        content_txt = ""
        for phase in phases:
            txt = phase.text.strip()
            if txt is not "":
                content_txt += txt + '\n'

        title_len = len(title_txt)
        content_len = len(content_txt)

        # 500 글자 이내의 컨텐츠 삭제
        if content_len < global_value.MIN_CONTENT_LEN:
            return

        # print(url)
        # print(title_txt, title_len)
        # print(content_txt, content_len)
        # print(has_vod, source_txt)

        # save news-content into file system
        try:
            path = global_value.OUTPUT_PATH + category
            if not os.path.isdir(path):
                os.mkdir(path)

            path = path + '/' + date
            if not os.path.isdir(path):
                os.mkdir(path)

            file = open(path + '/' + id + '.json', 'w', encoding='utf8')
            file.write(json.dumps({'title': title_txt, 'content': content_txt}, ensure_ascii=False))
            file.close()

        except Exception as e:
            logging.error('News data save error: ', e)

        # insert news-info into mysql
        try:
            conditional_query = 'id = %s '
            news_cnt = self.mysql_db.select_count('daum_news_'+category, conditional_query, 'id', id=id)
            if news_cnt == 0:
                rst = self.mysql_db.insert_news(id=id, category=category, date=date, link=link, has_vod=has_vod,
                                                source=source_txt, title_len=title_len, content_len=content_len)
                if rst == -1:
                    logging.error("MySQL insert error : id " + id)

        except Exception as e:
            logging.error('News info insert error: ', e)

    def check_title(self, title):
        # 영어 제목
        # 제목 10자 이상만
        # [기고문][인사][부고][인물광장][카드뉴스]
        # 제목이 ‘[‘ 이걸로 시작해서 ‘]’ 이걸로 끝나는거
        # 제목이 ‘\”‘ 이걸로 시작해서 ‘\”’ 이걸로 끝나는거
        # 제목이 ‘\’‘ 이걸로 시작해서 ‘\’’ 이걸로 끝나는거

        title = title.strip()

        regex = r'[가-힣]+'
        result = re.findall(regex, title)
        if len(result) is 0:
            return False

        if len(title) < global_value.MIN_TITLE_LEN:
            return False

        terms = global_value.BANNED_TITLE
        for term in terms:
            if term in title:
                return False

        if title.startswith('[') and title.endswith(']'):
            return False

        # if title.startswith('\'') and title.endswith('\''):
        #     return False
        #
        # if title.startswith('\"') and title.endswith('\"'):
        #     return False

        return True

    def run(self):
        self.crawl()


def main():
    log.init_log("logs/crawler", level=logging.INFO)
    logging.getLogger(__name__)

    parser = argparse.ArgumentParser(prog='crawler')
    parser.add_argument("-c", "--conf", help="config file path", required=True)
    args = parser.parse_args()

    # init global variables
    try:
        ret_conf = config_load.conf_parser(args.conf)
        logging.info("Read conf Success!!")
    except UnboundLocalError as msg:
        logging.error("Read conf fail. Message: %s" % msg)
        sys.exit(-1)
    else:
        if ret_conf is False:
            sys.exit(0)

    mysql_db = mysql.MysqlPython(host=global_value.MYSQL_HOST,
                                 user=global_value.MYSQL_USER,
                                 password=global_value.MYSQL_PASSWORD,
                                 database=global_value.MYSQL_DATABASE)
    Crawler(mysql_db).run()


if __name__ == "__main__":
    main()
