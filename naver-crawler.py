# -*- coding: UTF-8 -*-

import argparse
import logging
import queue
import os
import sys
import threading
import time
import requests
from bs4 import BeautifulSoup, Tag
import json
import config_load
import global_value
from utils import date_range, log, mysql
import re

# 테스트를 위해 만든 파일(함수로만)


def run():
# for category in global_value.CATEGORY_LIST:
#     days = date_range.getTimeTuple(global_value.START_DATE, global_value.END_DATE, 'D')
#     for day in days:
#         date = time.strftime('%Y%m%d', day)
        category = '107'
        date = '20170829'

        if category == '106':
            url = global_value.ENTER_JSON_URL + date
        else:
            url = global_value.BASE_LINKS_URL + "&sectionId=" + category + "&date=" + date
        try:
            # 연애일경우 json파일에 바로 접근하므로
            if category == '106':
                str_obj = requests.get(url).text
                json_obj = json.loads(str_obj)
                json_list = json_obj["articles"]
                links = []
                for link in json_list:
                    links.append(link["contentsArticle"]["linkUrl"])
            else:
                req = requests.get(url)
                html = req.text
                soup = BeautifulSoup(html, 'html.parser')
        except Exception as e:
            logging.error('News-links Request error: ', url, e)

        if category == '106': # 연애일경우 html파싱 필요없음
            pass
        else:
            try:
                no_ranking = soup.find('div', attrs={'class': 'no_ranking'})
                if no_ranking:
                    logging.error("Has no news-link from url: " + url)
                    # break

                links = []
                section = soup.find('div', attrs={'class': 'ranking_top3'})
                dt_list = section.findAll('dt')
                for dt in dt_list:
                    link = dt.find('a')['href']
                    links.append(link)

                section_list = soup.findAll('div', attrs={'class': 'ranking_section'})
                for section in section_list:
                    dt_list = section.findAll('dt')
                    for dt in dt_list:
                        link = dt.find('a')['href']
                        links.append(link)
            except Exception as e:
                logging.error('News-links HTML parse error: ', url, e)

        for link in links:
            # try:
            #     # 인덱스를 7, 14 늘리는건 위험할 수 있음?
            #     idx_oid = link.find('oid')
            #     oid = link[idx_oid:idx_oid + 7].split('=')[1]
            #     idx_aid = link.find('aid')
            #     aid = link[idx_aid:idx_aid + 14].split('=')[1]
            #     news_id = oid + aid
            try:
                # 스포츠일 경우 office_id
                if category == '107':
                    idx_oid = link.find('office_id')
                else:
                    idx_oid = link.find('oid')
                oid = link[idx_oid:].split('&')[0].split('=')[1]
                aid = link[idx_oid:].split('&')[1].split('=')[1]
                news_id = oid + aid
            except Exception as e:
                logging.error('News ID create error: ', e)

            try:
                # 스포츠일 경우 link가 http부터 들어가서 글로벌 변수 필요x
                if category == '107':
                    url = link
                elif category == '106':
                    url = global_value.ENTER_BASE_URL + link
                else:
                    url = global_value.BASE_NEWS_URL + link
                req = requests.get(url)
                html = req.text
                html = html.replace("<br>", "\n")
                soup = BeautifulSoup(html, 'html.parser')
            except Exception as e:
                logging.error('News Request error: ', url, e)

            try:
                # 연애 본문 파싱
                if category == '106':
                    title = soup.find('h2', attrs={'class': 'end_tit'})
                    content = soup.find('div', attrs={'id': 'articeBody'})
                    source_txt = soup.find('meta', attrs={'name': 'twitter:creator'})['content']
                # 스포츠 본문 파싱
                elif category == '107':
                    title = soup.find('h4', attrs={'class': 'title'})
                    content = soup.find('div', attrs={'id': 'newsEndContents'})
                    source = soup.find('meta', attrs={'property': 'og:article:author'})
                    source_txt = source.get('content').split('|')[1].strip()
                else:
                    title = soup.find('h3', attrs={'id': 'articleTitle'})
                    content = soup.find('div', attrs={'id': 'articleBodyContents'})
                    source = soup.find('meta', attrs={'property': 'me2:category1'})
                    source_txt = source.get('content').strip()

                title_txt = title.text.strip()
                for x in content.findAll('script'):
                    x.extract()
                for x in content.findAll('span'):
                    x.extract()
                for x in content.findAll('a'):
                    x.extract()
                for x in content.findAll('em'):
                    x.extract()

                has_vod = '0'
                if content.find('div', attrs={'class': 'vod_area'}) is not None:
                    has_vod = '1'

                for span in content.select('br'):
                    sup = soup.new_tag('p')
                    sup.string = '\n'
                    span.insert_after(sup)
                    span.unwrap()

                content_str = content.text
                phases = content_str.split('\n')
                content_txt = ""
                for phase in phases:
                    txt = phase.strip()
                    if txt is not "":
                        # '다.'로 끝나는 문장만 넣기
                        if "다." in txt:
                            content_txt += txt + '\n'

                print(title_txt)
                print(content_txt)
            except Exception as e:
                logging.error('News HTML parse error: ', url, e)

            # self.mysql_db.insert_news(id=news_id, category=category, date=date, link=link, has_vod=has_vod, source=source_txt)
            # save file
            try:
                path = global_value.OUTPUT_PATH + category
                if not os.path.isdir(path):
                    os.mkdir(path)

                path = path + '/' + date
                if not os.path.isdir(path):
                    os.mkdir(path)

                file = open(path + '/' + news_id + '.json', 'w', encoding='utf8')
                file.write(json.dumps({'title': title_txt, 'content': content_txt}, ensure_ascii=False))
                file.close()
            except Exception as e:
                logging.error('News data save error: ', e)

            # try:
            #     conditional_query = 'id = %s '
            #     news_cnt = self.mysql_db.select_count('naver_news', conditional_query, 'id', id=news_id)
            #     if news_cnt == 0:
            #         rst = self.mysql_db.insert_news(id=news_id, category=category, date=date, link=link, has_vod=has_vod, source=source_txt)
            #         if rst == -1:
            #             logging.error("MySQL insert error : id " + news_id)
            # except Exception as e:
            #     logging.error('News info insert error: ', e)

            time.sleep(global_value.CRAWL_INTERVAL)

        time.sleep(global_value.CRAWL_LONG_INTERVAL)

run()