# -*- coding: utf-8 -*-
from fake_useragent import UserAgent

ua = UserAgent()

BOT_NAME = 'anjukespider'

SPIDER_MODULES = ['anjukespider.spiders']
NEWSPIDER_MODULE = 'anjukespider.spiders'

# LOG_LEVEL = 'ERROR'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ua.random

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'anjukespider.middlewares.UserAgentMiddleware': 143,
#    'anjukespider.middlewares.IPProxyMiddleware': 1,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'anjukespider.middlewares.AnjukespiderDownloaderMiddleware': 543,
    'anjukespider.middlewares.UserAgentDownloaderMiddleware': 344,
    # 'anjukespider.middlewares.IPProxyDownloaderMiddleware': 343,
    'anjukespider.middlewares.FreeIPProxyDownloaderMiddleware': 342,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 使用ImagesPipeline
# 设置图片下载路径
IMAGES_STORE = 'F:\\Project\\Scrapy_anjuke\\anjukespider\\scene'
# 过期天数
# IMAGES_EXPIRES = 90  # 90天内抓取的都不会被重抓

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    # 'anjukespider.pipelines.DuplicatesPipeline': 100,
    'anjukespider.pipelines.DBPipeline': 110,
    'anjukespider.pipelines.AnjukeImgDownloadPipeline': 120,
    # 'anjukespider.pipelines.ImgDownloadPipeline': 120,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
