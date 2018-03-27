# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import re
from HW.items import HwItem
# 用户模块
#####
class HwSpider(scrapy.Spider):
    name = 'hw'
    allowed_domains = ['hihonor.com']
    start_urls = ['http://hihonor.com/']
    def start_requests(self):
        for i in range(9):
            base_url='https://club.hihonor.com/in/index-{}'
            yield Request(url=base_url.format(str(i+1)))
    def parse(self, response):
        user_urls=''.join(response.xpath('//a//@href').extract())
        u_template=re.compile(r'https://club.hihonor.com/in/(.*?)https')
        trg_id=u_template.findall(user_urls)
        trg_url=list(set(['https://club.hihonor.com/in/'+id for id in trg_id ]))
        for j in trg_url:
            k=j.split('javascript')[0]
            if 'https://club.hihonor.com/in/user/center/' not in k and len(k)>28:
                yield Request(url =k ,callback=self.content)
    def content(self,response):
        item=HwItem()
        title=''.join(response.xpath('//h2[@class="text-title"]//text()').extract())
        d_tempplate = re.compile('ON\s+(.*?\s+.*?\s+.*?\s+.*?\s+.*)')
        node_list=response.xpath('//div[@class="comment-list"]/ul/li')
        for node in node_list:
            user=node.xpath('./div[contains(@class,com-text)]//a/span[@class="name"]/text()').extract()
            tmp=''.join(node.xpath('./div[contains(@class,com-text)]//p[contains(@class,f-Comment)]//text()').extract()).replace('\n','').replace('\t','').replace('\r','').replace('\xa0','').replace('                              ','')
            content=tmp.split('#')[1]
            item['content']=content
            dates = ''.join(node.xpath('./div[contains(@class,com-text)]//p/text()').extract())
            if len(user) == 1:
                date = d_tempplate.findall(dates)
                if date:
                    item['date'] = date[0].replace('\r', '')
                item["user"] =user[0]
                item['title'] = title
                yield item
            elif len(user) > 1:
                for data in node.xpath('./div[contains(@class,com-text)]'):
                    dates = ''.join(data.xpath('.//p/text()').extract())
                    date=d_tempplate.findall(dates)
                    if date:
                        item['date']=date[0].replace('\r','')
                        print(item['date'])
                    name=data.xpath('.//a/span[@class="name"]/text()').extract()
                    if name:
                        item["user"]=name[0]
                    item['title'] = title
                    yield item



