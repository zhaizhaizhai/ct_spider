#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-05-09 20:58:34
# Project: nearby_ct1

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    i = 0   # i=0、1、2、3分别表示页面附近的第1，2，3，4个信息
    j = 0   # j=0、1、2分别表示附近的酒店、餐厅、景点
    ct_id = ""
    crawl_config = {
    }

    @every(minutes=240 * 60)
    def on_start(self):
        self.crawl('https://www.tripadvisor.cn/Restaurants-g294211-China.html', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.geo_image > a').items():
            self.crawl(each.attr.href, callback=self.index_page1)

    @config(age=10 * 24 * 60 * 60)
    def index_page1(self, response):
        string = response.doc('[name~=location]').attr("content")
        list = response.doc('[name~=description]').attr("content")
        id = response.url
        csid = (id.partition("Restaurants-")[2].partition("-"))[0][:]
        csend = (id.partition(csid + "-")[2].partition(".html"))[0][:]
        string = response.doc('[name~=location]').attr("content")
        list = response.doc('[name~=description]').attr("content")
        page1 = 0
        totalpages1 = 100
        num1 = 30
        urlstart1 = "https://www.tripadvisor.cn/Restaurants-" + csid + "-oa"
        urlend1 = "-" + csend + ".html"
        while page1 < totalpages1:
            self.crawl(urlstart1 + str(num1 * page1) + urlend1, callback=self.index_page2)
            page1 += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page2(self, response):
        for each in response.doc('.title > a').items():
            self.crawl(each.attr.href, callback=self.index_page3)

    @config(age=10 * 24 * 60 * 60)
    def index_page3(self, response):
        j = 1
        items = response.doc('.ui_section > .block_wrap > a').eq(j)
        self.crawl(items.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        i = 0
        items = response.doc('.location_name > a').eq(i)
        url = response.url
        name = items.text()
        ct0_id = (url.partition("-d")[2].partition("-"))[0][:]
        ct_id = (items.attr.href.partition("-d")[2].partition("-"))[0][:]
        distance = response.doc('b').eq(i).html()
        return {
            "name": name,
            "ct_id": ct_id,
            "ct0_id": ct0_id,
            "distance": distance

        }