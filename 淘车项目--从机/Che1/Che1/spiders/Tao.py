# -*- coding: utf-8 -*-
import scrapy
import socket
from Che1.items import Che1Item
from scrapy_redis.spiders import RedisSpider

class TaoSpider(RedisSpider):
    name = 'Che'
    count=1
    # allowed_domains = ['maoyan.com']
    # start_urls = ['https://maoyan.com/cinemas']
    redis_key = "taoche:start_urls"
    myname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    myaddr = socket.gethostbyname(myname)

    def parse(self, response):
        car_info_list = response.xpath("//ul[@class='gongge_ul']/li[@data-id]")
        # 遍历所有的车
        # 获取本机电脑名

        for car_info in car_info_list:
            title = car_info.xpath(".//span/text()").extract_first()  # 标题
            detail_url = car_info.xpath(".//a[@class='title']/@href").extract_first()  # 详情页url
            detail_url = "https:" + detail_url
            print(title,detail_url,print(self.myaddr))

            # 将所有的字段放入iten中
            item = Che1Item()
            item["ip"] = self.myaddr
            item["title"] = title
            item["detail_url"] = detail_url


            yield scrapy.Request(detail_url, callback=self.parse_detail, meta={"data": item}, dont_filter=True)

    def parse_detail(self, response):

        # print(item)
        # 获取详情页信息
        pic_list = response.xpath("//ul[@id='carSourceImgUl']/li/img/@src").extract()  # 图片
        pic = ["https:" + p for p in pic_list]
        # print(source_id,displace,pic)

        # 接收item
        item = response.meta["data"]
        item["pic"] = pic
        yield item

