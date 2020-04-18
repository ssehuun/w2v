# 프로젝트 설명

* 가짜뉴스 찾기 챌린지 (2017.08 ~ 2017.11)
* 공식 링크 - https://ezone.iitp.kr/common/anno/03/form.tab?PMS_PBNM_ID=PBN2017004
* 자연어 처리 모델 리서치 및 데이터 파이프라인 구축

#

## 디렉토리 설명

* global_value.py - 카테고리별 기사 분류 및 URL 관리

* global_value_except.py - 크롤링 하지 않아도 될 특징 예외처리

* config_load.py - 크롤링 작업 하기 전 config 설정 수행

* naver-crawler.py -  네이버 기사 크롤링 수행

* daum-crawler.py - 다음 기사 크롤링 수행

* tokenizer.py - 뉴스 기사를 단어단위로 토크나이징

* w2v.py - 단어를 벡터 공간에 사상 후 모델 생성

* utils - 전처리된 파일을 myql DB에 저장 및 로그 관리

  



