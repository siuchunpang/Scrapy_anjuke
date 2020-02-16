import requests
from fake_useragent import UserAgent
from scrapy.pipelines.images import ImagesPipeline
from anjukespider.model.scene import Scene
from anjukespider.model.config import DBSession
from anjukespider.model.config import Redis
from anjukespider.items import AnjukespiderItem, ImageItem
from scrapy.exceptions import DropItem
from scrapy import Request


# 数据去重
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.hexists("duplicate", item['scene_name']):
            print("Duplicate item found: %s" % item)
            raise DropItem("Duplicate item found: %s" % item)
        else:
            Redis.hset("duplicate", item['scene_name'], 1)
            return item


# 下载图片（自定义）
class ImgDownloadPipeline(object):
    def __init__(self):
        self.ua = UserAgent()

    # def get_html(self, url):
    #     USER_AGENT = self.ua.random
    #     headers = {
    #         "User-Agent": USER_AGENT,
    #         "Connection": "keep-alive",
    #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #         "Accept-Language": "zh-CN,zh;q=0.8"}
    #     resp = requests.get(url, headers=headers)
    #     html = resp.content
    #     return html

    # def process_item(self, item, spider):
    #     hotspots = item["hotspots"]
    #     print(hotspots)
    #     for hotspots_index, hotspot in enumerate(hotspots):
    #         img_urls = hotspot['TileImagesPath']
    #         scene_name = item["scene_name"]
    #         scene_path = "F:\\Project\\Scrapy_anjuke\\anjukespider\\scene\\"
    #         # img_count = item["img_count"]
    #         # 创建场景文件夹
    #         if not os.path.exists(scene_path + scene_name):
    #             print('创建文件夹:%s' % scene_name)
    #             os.mkdir(scene_path + scene_name)
    #             # print("开始解析图片%d..." % img_count)
    #             # img_count += 1
    #             # 创建热点文件夹
    #             if not os.path.exists(scene_path + "%s\\hotspot_%s" % (scene_name, hotspots_index)):
    #                 # print('创建文件夹:hotspot_%s' % hotspots_index)
    #                 os.mkdir(scene_path + "%s\\hotspot_%s" % (scene_name, hotspots_index))
    #
    #                 for img_links_index, img_link in enumerate(img_urls):
    #                     img_link_name = img_link[24:56]
    #                     # print("图片名称:%s_%d.jpg" % (img_link_name, img_links_index))
    #                     html = self.get_html(img_link)
    #                     with open(scene_path + "hotspot_%s\\%s_%d.jpg" % (hotspots_index, img_link_name, img_links_index),
    #                               'wb') as file:
    #                         file.write(html)


# 下载图片（自带）
class AnjukeImgDownloadPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        img_url = item["img_url"]
        img_link_name = img_url[24:56]
        return 'full/hotspot_%s/%s_%s' % (item["hotspots_index"], img_link_name, item["img_index"])

    def get_media_requests(self, item, info):
        isImageItem = isinstance(item, ImageItem)
        if isImageItem:
            image_urls = item['image_urls']
            for image_url in image_urls:
                # item["img_index"] = img_index
                yield Request(image_url, meta={'item': item, 'img_url': image_url,  'index': item['image_urls'].index(image_url)})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item


# 数据库操作
class DBPipeline(object):
    def __init__(self):
        self.session = DBSession()

    def process_item(self, item, spider):
        if isinstance(item, AnjukespiderItem):
            sql = Scene(
                scene_name=item["scene_name"],
                web_site=item["web_site"],
                link_3d=item["link_3d"],
                creat_time=item["creat_time"]
            )
            self.session.add(sql)
            self.session.commit()

    def close_spider(self, spider):
        self.session.close()
