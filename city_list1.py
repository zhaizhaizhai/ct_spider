#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-04-23 00:33:24
# Project: city_list1

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=240 * 60)
    def on_start(self):
        self.crawl('https://www.tripadvisor.cn/Restaurants-g294211-China.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.geo_image > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        string = response.doc('[name~=location]').attr("content")
        list = response.doc('[name~=description]').attr("content")
        id = response.url

        return {
            "csid": (id.partition("Restaurants-")[2].partition("-"))[0][:],
            "sfname": (string.partition("province=")[2].partition(";city="))[0][:],
            "csname": (string.partition(";city=")[2].partition(";coord="))[0][:],
            "ctnum ": (list.partition("美食餐饮，")[2].partition("家"))[0][:],
            "dpnum ": (list.partition("餐厅，")[2].partition("篇"))[0][:],
        }