# -*- coding: utf-8 -*-

# Scrapy settings for posts project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'cnbeta_robot_test'

SPIDER_MODULES = ['posts.spiders']
NEWSPIDER_MODULE = 'posts.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'posts (+http://www.yourdomain.com)'

# DOWNLOAD_DELAY = 2
# RANDOMIZE_DOWNLOAD_DELAY = True
RANDOMIZE_DOWNLOAD_DELAY = False

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = True

ITEM_PIPELINES = {
    'posts.pipelines.PostsPipeline': 300,
    'posts.pipelines.SQLStorePipeline': 800,
}

LOG_LEVEL = 'INFO'

# LOG_FILE = 'log.txt'


CONCURRENT_ITEMS = 100

CONCURRENT_REQUESTS = 20

CONCURRENT_REQUESTS_PER_DOMAIN = 8

CONCURRENT_REQUESTS_PER_IP = 0
