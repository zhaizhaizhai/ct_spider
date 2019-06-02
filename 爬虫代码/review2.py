#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-05-09 16:35:48
# Project: review2
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
        for each in response.doc('.pageNumbers > a').items():
            self.crawl(each.attr.href, callback=self.index_page4)

    @config(age=10 * 24 * 60 * 60)
    def index_page4(self, response):
        for each in response.doc('.quote > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        pl_id = (url.partition("-r")[2].partition("-"))[0][:]
        ct_id = (url.partition("-d")[2].partition("-"))[0][:]
        title = response.doc('#PAGEHEADING').text()
        pl0 = response.doc('#review_' + pl_id).filter('.mgrRspnInline')

        respon = ""
        isrespon = 0
        if pl0.length != 0:
            isrespon = 1
            respon = pl0.filter('.partial_entry').text()
        pl = response.text
        if isrespon == 1:
            respon = (pl.partition("用餐日期：</span>"))[2].partition("<")[0][:]
        eat_date = (pl.partition("用餐日期：</span>"))[2].partition("<")[0][:]
        pl_date = (pl.partition('"ratingDate relativeDate"' + " title='"))[2].partition("'>")[0][:]
        plr_id = (pl.partition("name_click')" + '">'))[2].partition("</")[0][:]
        fxnum = (pl.partition('badgetext">'))[2].partition("</")[0][:]
        gxnum = (pl.partition('ui_icon thumbs-up-fill"></span><span class="badgetext">'))[2].partition("</")[0][:]
        score = (pl.partition('ui_bubble_rating bubble_'))[2].partition('0"')[0][:]
        content = (pl.partition('partial_entry">'))[2].partition('</')[0][:]

        return {

            "pl_id": pl_id,
            "ct_id": ct_id,
            "eat_date": eat_date,
            "pl_date": pl_date,
            "plr_id": plr_id,
            "fxnum": fxnum,
            "gxnum": gxnum,
            "score": score,
            "title": title,
            "content": content,
            "isrespon": isrespon,
            "respon": respon
        }