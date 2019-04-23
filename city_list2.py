#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-04-21 18:08:13
# Project: city_list2

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.page = 0
        self.totalpages = 45
        self.num = 20
        self.urlstart = "https://www.tripadvisor.cn/Restaurants-g294211-oa"
        self.urlend = "-China.html"

    @every(minutes=24 * 60)
    def on_start(self):
        while self.page < self.totalpages:
            self.crawl(self.urlstart + str(20 + self.num * self.page) + self.urlend, callback=self.index_page)
            self.page += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('#LOCATION_LIST .geoList li a').items():
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