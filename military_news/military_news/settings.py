# -*- coding: utf-8 -*-

# Scrapy settings for military_news project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import os

BOT_NAME = 'military_news'

SPIDER_MODULES = ['military_news.spiders']
NEWSPIDER_MODULE = 'military_news.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'military_news.middlewares.MilitaryNewsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'military_news.middlewares.MilitaryNewsDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
  #  'military_news.pipelines.MilitaryNewsPipeline': 300,
  #  'military_news.pipelines.NewsCsvPipeline': 300,
  'military_news.pipelines.MySQLPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# MYSQL_HOST = 'localhost'
# MYSQL_DATABASE = 'military'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# # MYSQL_PASSWORD = ''
# MYSQL_PASSWORD = 'maxiaoteng'

MYSQL_HOST = 'localhost'
MYSQL_DATABASE = 'news'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
# MYSQL_PASSWORD = ''
MYSQL_PASSWORD = 'PnS_cDEZhMb4p8M3'


# 配置log
logFilename = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../log/military.log')

log_dir = os.path.split(logFilename)[0]
if not os.path.exists(log_dir):
  os.makedirs(log_dir)
logging.basicConfig(
  level = logging.DEBUG,  # 定义输出到文件的log级别，
  format = '%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
  datefmt= '%Y-%m-%d %A %H:%M:%S',  # 时间
  filename = logFilename,  # log文件名
  filemode = 'w')

FEED_EXPORT_ENCODING = 'UTF-8'

# 设置超时，默认180秒
DOWNLOAD_TIMEOUT = 10