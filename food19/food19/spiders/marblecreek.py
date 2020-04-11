# -*- coding: utf-8 -*-
import scrapy
from food19.items import Food19Item


class MarblecreekSpider(scrapy.Spider):
    name = 'marblecreek'
    allowed_domains = ['marblecreekfarmstead.com']
    start_urls = [
        'https://marblecreekfarmstead.com/collections/frontpage',
        'https://marblecreekfarmstead.com/collections/grass-fed-beef',
    ]

    def parse(self, response):
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
