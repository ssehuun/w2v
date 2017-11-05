# -*- coding: UTF-8 -*-

import os
import json
import logging
import logging.handlers
import re
import itertools


DIR_PATH = '../data_parse/'
CATEGORY_LIST = ['100', '101', '102', '103', '104', '105', '106', '107']
#정치 경제 사회 생활/문화 세계 IT/과학 연예 스포츠
CATEGORY_LIST1 = ['101']
CATEGORY_LIST2 = ['101', '107']

# 같은 분야에서 기사 뽑기
def getSameField():
    # date list
    total_list = []
    tokenized_list = []

    for category in CATEGORY_LIST1:
        date_list = os.listdir(DIR_PATH + category)

        category_path = DIR_PATH + category
        news_list = []

        # 101분야에서 날짜별로 모든 json 파일이 news_list에 저장
        # 180일치만
        # for date in itertools.islice(date_list, 0, 180):
        for date in date_list:
            article_list = os.listdir(category_path+'/'+date)
            for article in article_list:
                news_list.append(category_path+'/'+date+'/'+article)

        # print(len(news_list)) 개수확인

        total_txt = ""
        for news in news_list:
            with open(news, encoding='utf8') as json_data:
                dic = json.load(json_data)

                content = dic['content']
                # print(content)

                # 기사 본문에서 문단을 합치고 "다"로 안끝나는 것들을 뺌
                paragraphs_list = content.split('\n')
                content_txt = ""
                for paragraph in paragraphs_list:
                    if "다." in paragraph:
                        # 정규식 파싱
                        paragraph = re.sub('[\[(【=][^(【\[]+[)\]】]', '', paragraph)
                        content_txt += paragraph
                content_txt += content_txt + '\n'
            total_txt += content_txt

        savefile(total_txt, category)


        '''
        # 다시 "." 문장 단위로 나누고 리스트에 넣는다
        sent_list = content_txt.split(".")

        sent_pretty_list = []
        for sent in sent_list:
            if len(sent) > 1:
                sent_pretty_list.append(sent.strip())
        # print(len(sent_list), sent_pretty_list)


        # 여기서 단어단위로 토크나이징 시작
        # if len(pretty_list) > 1:
        #     for sen in pretty_list:
        #         if len(twitter.nouns(sen)) > 0:
        #             tokenized_list.append(twitter.nouns(sen))

            # total_list.append(tokenized_list)
        # savefile1(total_list, category)
    # print(total_list)
'''

# save file
def savefile(data, category):
    try:
        with open("./"+category+"_Economy.txt", "a", encoding='utf8') as text_file:
            text_file.write(data)
    except Exception as e:
        logging.error('File not saved: ', e)





if __name__ == '__main__':
    getSameField()

    '''
    로그 남길시 이용
    logger = logging.getLogger('mylogger')
    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    fileHandler = logging.FileHandler('./myLoggerTest.log')
    streamHandler = logging.StreamHandler()

    fileHandler.setFormatter(fomatter)
    streamHandler.setFormatter(fomatter)

    logger.addHandler(fileHandler)
    logger.addHandler(streamHandler)

    logger.setLevel(logging.DEBUG)
    # logger.error("파일로도 남으니 안심이죠~!")
    # logger.critical("치명적인 버그는 꼭 파일로 남기기도 하고 메일로 발송하세요!")

    logger.debug("===========================")
    logger.info("TEST START")

    getSameField()

    logger.debug("===========================")
    logger.info("TEST END!")
    '''

