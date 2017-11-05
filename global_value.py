import queue
import threading

# global variables
BASE_NEWS_URL = 'http://news.naver.com/'
BASE_LINKS_URL = 'http://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day'

ENTER_BASE_URL = 'http://entertain.naver.com/ranking/'
ENTER_LINKS_URL = 'http://entertain.naver.com/ranking?rankingType=popular_day'
ENTER_JSON_URL = 'http://entertain.naver.com/ranking/page.json?&type=default&date='

CATEGORY_LIST = ['100', '101', '102', '103', '104', '105', '106', '107']
# 정치 경제 사회 생활/문화 세계 IT/과학 연예 스포츠
START_DATE = ''
END_DATE = ''
CRAWL_INTERVAL = 0
CRAWL_LONG_INTERVAL = 0
OUTPUT_PATH = ''
QUEUE_MAX_SIZE = 1500

MYSQL_HOST = ''
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DATABASE = ''

LOCK = threading.Lock()
URL_QUEUE = queue.Queue()
CRAWED_URLS = set()