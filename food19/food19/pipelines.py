# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class Food19Pipeline(object):
    def process_item(self, item, spider):
        if item.get('product_name'):
            return item
        else:
            DropItem("Missing product name")
