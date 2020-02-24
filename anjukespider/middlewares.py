# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time
import logging
import requests
from scrapy import signals
from fake_useragent import UserAgent
from selenium import webdriver

"""
class AnjukespiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AnjukespiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
"""


class UserAgentDownloaderMiddleware(object):
    url = ""

    def process_request(self, request, spider):
        ua = UserAgent()
        user_agent = ua.random
        request.headers['User-Agent'] = user_agent
        self.url = request.url

    def process_response(self, request, response, spider):
        if ".jpg" not in request.url:
            error_element = response.xpath('/html/head/title').get()
            error_name = "访问验证-安居客"
            if error_name in error_element:
                # logging.warning("反爬机制已阻拦，需要人工操作")
                print("反爬机制已阻拦，需要人工操作")
                driver = webdriver.Chrome()
                driver.get(self.url)
                driver.maximize_window()
                time.sleep(10)
                driver.close()
                # logging.info("解除反爬机制")
                print("解除反爬机制")
                # with open("error.txt", "w", encoding='utf-8') as file:
                #     file.write(response.text)
                return request
            else:
                return response
        else:
            return response


'''
class IPProxyDownloaderMiddleware(object):
    def get_proxy(self):
        return requests.get("http://127.0.0.1:5010/get/").json()

    def delete_proxy(self, proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    def identify_proxy(self):
        proxy = self.get_proxy().get("proxy")
        html = requests.get("http://httpbin.org/get", timeout=5, proxies={"http": "http://{}".format(proxy)})
        html.encoding = 'utf-8'
        html_text = html.text
        if "违规网站" in html_text:
            self.delete_proxy(proxy)
        else:
            return proxy

    def process_request(self, request, spider):
        proxy = self.identify_proxy()
        request.meta['proxy'] = "http://{}".format(proxy)


class FreeIPProxyDownloaderMiddleware(object):
    def get_proxy(self):
        proxy = requests.get("https://www.freeip.top/api/proxy_ip").json()
        ip = proxy["data"].get("ip")
        port = proxy["data"].get("port")
        return ip + ":" + port

    def process_request(self, request, spider):
        proxy = self.get_proxy()
        print("代理IP为：", proxy)
        request.meta['proxy'] = "http://{}".format(proxy)
'''
