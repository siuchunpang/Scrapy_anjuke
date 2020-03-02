import json
import os
import logging

from scrapy.pipelines.files import FilesPipeline
from anjukespider.model.scene import Scene, SceneImg
from anjukespider.model.config import DBSession
from anjukespider.model.config import Redis
from anjukespider.settings import FILES_STORE
from scrapy.exceptions import DropItem
from scrapy import Request

Duplicate_item = 0


# 数据去重
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.hexists("duplicate", item['scene_unique_name']):
            global Duplicate_item
            Duplicate_item += 1
            print("重复数据:%d" % Duplicate_item)
            raise DropItem("Duplicate item found: %s" % item)
        else:
            Redis.hset("duplicate", item['scene_unique_name'], 1)
            return item


# 下载图片（自带）
class ImgDownloadPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file_url = request.url
        file_link_name = file_url[24:56]
        return '%s/picture/%s.jpg' % (item["scene_unique_name"], file_link_name)

    def get_media_requests(self, item, info):
        if item["link_3d"] != "":
            for hotspot in item["hotspots"]:
                file_urls = hotspot['TileImagesPath']
                for file_url in file_urls:
                    yield Request(url=file_url, meta={'item': item})

    def item_completed(self, results, item, info):
        if item["link_3d"] != "":
            print("图片下载完毕")
            item["results"] = results
            file_paths = [x['path'] for ok, x in results if ok]
            # logging.info("file_paths：", file_paths)
            print("file_paths：", file_paths)
            if not file_paths:
                raise DropItem("Item contains no images")
            item['file_paths'] = file_paths
        return item


# 下载Json文件
class JsonDownloadPipeline(object):
    def process_item(self, item, spider):
        if item["link_3d"] != "":
            scene_path = FILES_STORE + item["scene_unique_name"]
            if not os.path.exists(scene_path + "\\scene.json"):
                # logging.info("下载Json文件")
                print("下载Json文件")
                try:
                    item["error"] = None
                    with open(scene_path + "\\scene.json", 'w') as file:
                        json.dump(item["data"], file)
                except FileNotFoundError as e:
                    item["error"] = e
        return item


# 数据库操作
class DBPipeline(object):
    def __init__(self):
        self.session = DBSession()

    def process_item(self, item, spider):
        try:
            if item["link_3d"] != "" and item["error"] is None:
                # logging.info("录入数据库")
                print("录入scene表")
                sql_scene = Scene(
                    scene_unique_name=item["scene_unique_name"],
                    scene_name=item["scene_name"],
                    web_site=item["web_site"],
                    link_3d=item["link_3d"],
                    shoot_count=item["shoot_count"],
                    creat_time=item["creat_time"]
                )
                self.session.add(sql_scene)
                self.session.flush()

                # logging.info("录入数据库")
                print("录入scene_img表")
                for i, hotspot in enumerate(item["hotspots"]):
                    file_urls = hotspot['TileImagesPath']
                    for j, img_url in enumerate(file_urls):
                        sql_img = SceneImg(
                            scene_id=sql_scene.id,
                            img_url=img_url,
                            is_downloaded=item["results"][i*6+j][0],
                            failed_download_reason=str(item["results"][i*6+j][1])
                        )
                        self.session.add(sql_img)
                self.session.commit()
            else:
                print("录入scene表")
                sql_scene = Scene(
                    scene_unique_name=item["scene_unique_name"],
                    scene_name=item["scene_name"],
                    web_site=item["web_site"],
                    link_3d=item["link_3d"],
                    shoot_count=0,
                    creat_time=item["creat_time"]
                )
                self.session.add(sql_scene)
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            # logging.error("DBPipeline_error：", e)
            print("DBPipeline_error：", e)
        return item

    def close_spider(self, spider):
        print("共爬取%d个场景" % spider.scene_count)
        self.session.close()

