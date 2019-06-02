#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-04-23 00:59:16
# Project: ct_list1

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
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        url = response.url
        id = (url.partition("Review-")[2].partition("Reviews"))[0][:]
        ct_id = (id.partition("-")[2].partition("-"))[0][:]
        name = response.doc('.h1').text()
        rank1 = response.doc('.restaurants-detail-overview-cards-RatingsOverviewCard__ranking--17CmN').text()
        rank = (rank1.partition("排名第")[2].partition("的"))[0][:] + (rank1.partition("美食")[2].partition(")"))[0][:]
        tag = response.doc('.restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h').text()

        score = response.doc(
            '.restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl').text() + '(满分5.0)'
        address1 = response.doc('.restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei').text()
        address = (address1.partition("+"))[0][:]
        sf_name = (address.partition(" "))[0][:]
        city_name = (address.partition(" ")[2].partition(" "))[0][:]
        phone = response.doc('.detail.is-hidden-mobile').text()
        return {
            "ct_id": ct_id,
            "name": name,
            "tag": tag,
            "score": score,
            "address": address,
            "sf_name": sf_name,
            "city_name": city_name,
            "phone": phone,
            "rank": rank
        }

