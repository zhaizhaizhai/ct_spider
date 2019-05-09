#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-05-09 19:46:32
# Project: nearby_hotel2

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    i = 0  # i=0、1、2、3分别表示页面附近的第1，2，3，4个信息
    j = 0  # j=0、1、2分别表示附近的酒店、餐厅、景点
    crawl_config = {
    }

    def __init__(self):
        self.page = 0
        self.totalpages = 45
        self.num = 20
        self.urlstart = "https://www.tripadvisor.cn/Restaurants-g294211-oa"
        self.urlend = "-China.html"

    @every(minutes=240 * 60)
    def on_start(self):
        while self.page < self.totalpages:
            self.crawl(self.urlstart + str(20 + self.num * self.page) + self.urlend, callback=self.index_page)
            self.page += 1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('#LOCATION_LIST .geoList li a').items():
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
        items = response.doc('.ui_section > .block_wrap > a').eq(0)
        self.crawl(items.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        i = 0
        items = response.doc('.listing_title > a').eq(i)
        url = response.url
        name = items.text()
        ct_id = (url.partition("-d")[2].partition("-"))[0][:]
        hotel_id = (items.attr.href.partition("-d")[2].partition("-"))[0][:]
        distance = response.doc('b').eq(i).html()
        return {
            "name": name,
            "hotel_id": hotel_id,
            "ct_id": ct_id,
            "distance": distance

        }