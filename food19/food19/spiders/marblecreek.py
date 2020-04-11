# -*- coding: utf-8 -*-
import scrapy
from food19.items import Food19Item


class MarblecreekSpider(scrapy.Spider):
    name = 'marblecreek'
    allowed_domains = ['marblecreekfarmstead.com']
    start_urls = [
        'https://marblecreekfarmstead.com/collections/',
  #      'https://marblecreekfarmstead.com/collections/grass-fed-beef',
   #     'https://marblecreekfarmstead.com/collections/pastured-chicken',
    #    'https://marblecreekfarmstead.com/collections/pastured-pork',
     #   'https://marblecreekfarmstead.com/collections/pastured-goat-and-grassfed-lamb',
    ]
    collection_urls = []

    def parse(self, response):
        if response.css('h1::text').get() == 'Collections':
            self.collection_urls = self.find_collection_urls(response)
            yield self.collection_urls.pop()

        products = response.css('div.grid-view-item')
        for product in products:
            item = Food19Item()

            # Find the name of the product
            product_name = product.css('div.product-card__title::text').get()
            item['product_name'] = product_name

            # Find the regular price of the product
            product_price = product.css('span.price-item--regular::text').get()
            product_price = product_price.strip()
            item['price'] = product_price.strip('$')

            product_sale = product.css('span.price-item--sale::text').get()
            product_sale = product_sale.strip()
            item['sale_price'] = product_sale.strip('$')
            yield item
        if self.collection_urls:
            yield scrapy.Request(url=self.collection_urls.pop(), callback=self.parse)

    def find_collection_urls(self, response):
        collections = response.css('a::attr(href)')
        links = response.xpath("//a/@href").getall()
        valid_urls = []
        for link in links:
            if 'collection' in link:
                valid_urls.append('https://marblecreekfarmstead.com' + link)
        return valid_urls
