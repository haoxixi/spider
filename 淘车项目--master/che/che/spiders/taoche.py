# -*- coding: utf-8 -*-
import scrapy
from che.spiders.city import CITY_CODE, CAR_CODE_LIST
from che.items import CheItem
from scrapy_redis.spiders import RedisSpider


class TaocheSpider(RedisSpider):
    name = 'taoche'
    # allowed_domains = ['taoche.com']
    # start_urls = []
    # start_urls = ["https://beijing.taoche.com/volkswagen/"]
    # start_urls = ["https://beijing.taoche.com/astonmartin/"]
    redis_key = "taoche:start_urls"
    # 将所有的城市 所有的品牌写入start_urls中
    for city in CITY_CODE:
        for car_code in CAR_CODE_LIST:
            base_url = "https://{}.taoche.com/{}/".format(city, car_code)
            # print(base_url)
            # start_urls.append(base_url)

    # print(len(start_urls))

    # 获取翻页的url
    def parse(self, response):
        # 获取最大页数
        max_page_list = response.xpath("//div[@class='paging-box the-pages']/div/a[last()-1]/text()").extract()
        max_page = int(max_page_list[0]) if max_page_list else 1

        # 遍历所有的页码进行爬取
        for page in range(max_page):
            base_url = response.url + "?page={}#pagetag".format(page + 1)
            # print(base_url)
            yield scrapy.Request(url=base_url, callback=self.parse_list, dont_filter=True)

    def parse_list(self, response):

        # 缩小范围
        car_info_list = response.xpath("//ul[@class='gongge_ul']/li[@data-id]")

        # print(len(car_info_list))
        # 遍历所有的车，获取列表页当中的数据
        for car_info in car_info_list:

            title = car_info.xpath(".//span/text()").extract_first()  # 标题
            reg_date = car_info.xpath(".//p/i[1]/text()").extract_first()  # 上牌日期
            mile = car_info.xpath(".//p/i[2]/text()").extract_first()
            city_name = car_info.xpath(".//p/i[3]/a/text()").extract_first()
            price = car_info.xpath(".//div[@class='price']/i[1]/text()").extract_first()
            all_price = car_info.xpath(".//div[@class='price']/i[2]/text()").extract()
            all_price = all_price[0] if all_price else ''
            detail_url = car_info.xpath(".//a[@class='title']/@href").extract_first()
            detail_url = "https:" + detail_url

            # 将所有的抓取字段放入 item中
            item = CheItem()
            item["title"] = title
            item["reg_date"] = reg_date
            item["mile"] = mile
            item["city_name"] = city_name
            item["price"] = price
            item["all_price"] = all_price
            item["detail_url"] = detail_url

            # 获取详情页信息
            yield scrapy.Request(detail_url, callback=self.parse_detail,
                                 meta={"data": item}, dont_filter=True)

    # 解析详情页
    def parse_detail(self, response):

        # 接收item
        item = response.meta["data"]

        # 获取详情页的抓取字段
        source_id = response.xpath("//span[@class='car-number']/text()").extract_first()  # 车源id
        displace = response.xpath("//div[@class='col-xs-6 parameter-configure-list'][2]/ul/li[1]/span/a/text()").extract_first()  # 排量
        pic_list = response.xpath("//ul[@id='carSourceImgUl']/li/img/@data-src").extract()
        # pic = []
        # for p in pic_list:
        #     p = "https:" + p
        #     pic.append(p)
        pic = ["https:" + p for p in pic_list]

        item["source_id"] = source_id
        item["displace"] = displace
        item["pic"] = pic
        # print(item)
        yield item




'''
    title = scrapy.Field()  # 标题
    reg_date = scrapy.Field()   # 上牌日期
    mile = scrapy.Field()   # 公里数
    city_name = scrapy.Field()   # 城市名称
    price = scrapy.Field()  # 优惠价格
    all_price = scrapy.Field()   # 全款价格
    pic = scrapy.Field()   # 图片
    displace = scrapy.Field()   # 排量
    source_id = scrapy.Field()  # 车源号
'''

