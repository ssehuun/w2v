import queue
import threading

# global variables
BASE_LINKS_URL = 'http://media.daum.net/breakingnews/'
BASE_NEWS_URL = 'http://v.media.daum.net/v/'
CATEGORY_LIST = []
START_DATE = ''
END_DATE = ''
CRAWL_INTERVAL = 0
CRAWL_LONG_INTERVAL = 0
OUTPUT_PATH = ''

MIN_TITLE_LEN = 10
BANNED_TITLE = ["[기고문]", "[인사]", "[부고]", "[인물광장]", "[카드뉴스]"]
MIN_CONTENT_LEN = 500


MYSQL_HOST = ''
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DATABASE = ''

LOCK = threading.Lock()
URL_QUEUE = queue.Queue()
CRAWED_URLS = set()

