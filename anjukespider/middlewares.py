# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time
from fake_useragent import UserAgent
from selenium import webdriver


class UserAgentDownloaderMiddleware(object):

    def process_request(self, request, spider):
        ua = UserAgent()
        user_agent = ua.random
        request.headers['User-Agent'] = user_agent

    def process_response(self, request, response, spider):
        if ".jpg" not in request.url:
            error_element = response.xpath('/html/head/title').get()
            error_name = "访问验证-安居客"
            if error_name in error_element:
                # logging.warning("反爬机制已阻拦，需要人工操作")
                print("反爬机制已阻拦，需要人工操作")
                driver = webdriver.Chrome()
                driver.get(request.url)
                driver.maximize_window()
                time.sleep(8)
                driver.close()
                # logging.info("解除反爬机制")
                print("解除反爬机制")
                origin_url = request.meta["redirect_urls"][0]
                request._set_url(origin_url)
                return request
            else:
                return response
        else:
            return response


class RandomDelayMiddleware(object):
    def __init__(self):
        self.delay = 3

    def process_request(self, request, spider):
        delay = random.randint(0, self.delay)
        print("延迟访问")
        time.sleep(delay)
