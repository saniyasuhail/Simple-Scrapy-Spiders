# -*- coding: utf-8 -*-
import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['www.tinydeal.com.hk']
    #start_urls = ['https://www.tinydeal.com.hk/specials.html']

    def start_requests(self):
        url='https://www.tinydeal.com.hk/specials.html'
        
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
            }                                                                                           
        yield scrapy.Request(url,headers=headers,callback=self.parse)

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/li"):
            yield{
                'title':product.xpath(".//a[@class='p_box_title']/text()").get(),
                'url':response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                'discounted_price':product.xpath(".//div[@class='p_box_price']/span[1]/text()").get(),
                'original_price':product.xpath(".//div[@class='p_box_price']/span[2]/text()").get(),
                'User-Agent':response.request.headers['User-Agent']
            }
            

        next_page = response.xpath("//a[@class='nextPage']/@href").extract_first()   

        if next_page:
            yield scrapy.Request(url=next_page,callback=self.parse,dont_filter=True,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'})