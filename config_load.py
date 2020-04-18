import configparser as ConfigParser
import logging
import os

import global_value

def conf_parser(conf_file):
    logger = logging.getLogger(__name__)

    if not os.path.exists(conf_file):
        logging.error("Config file %s doesn't exist!" % (conf_file))
        return False

    config = ConfigParser.ConfigParser()
    config.read(conf_file)

    try:
        global_value.CATEGORY_LIST = config.get('crawler', 'category_list').split(',')
        global_value.START_DATE = config.get('crawler', 'start_date')
        global_value.END_DATE = config.get('crawler', 'end_date')
        global_value.CRAWL_INTERVAL = config.getfloat('crawler', 'crawl_interval')
        global_value.CRAWL_LONG_INTERVAL = config.getfloat('crawler', 'crawl_long_interval')
        global_value.OUTPUT_PATH = config.get('crawler', 'output_path')

        global_value.MYSQL_HOST = config.get('mysql', 'host')
        global_value.MYSQL_USER = config.get('mysql', 'user')
        global_value.MYSQL_PASSWORD = config.get('mysql', 'password')
        global_value.MYSQL_DATABASE = config.get('mysql', 'database')

        logger.info("Read global values from %s successfully" % (conf_file))

        # check config is legal
        return check_config()
    except (ValueError, ConfigParser.NoOptionError) as err:
        logger.error("Read global value error, Error message: %s ", err)
        return False


def check_config():
    logger = logging.getLogger(__name__)
    """
    check config is legal
    """
    if not isinstance(global_value.CRAWL_INTERVAL, float) or global_value.CRAWL_INTERVAL < 0:
        logger.error("the config of crawl_interval is illegal.")
        return False
    if len(global_value.CATEGORY_LIST) < 1 :
        logger.error("the category_list is illegal.")
        return False
    return True

