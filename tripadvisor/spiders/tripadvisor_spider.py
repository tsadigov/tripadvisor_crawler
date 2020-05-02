import scrapy
import re, math
from scrapy.loader import ItemLoader
from tripadvisor.items import RestaurantItem, RestaurantInfoItem, RestaurantReviewItem
import sys, os

class TripadvisorSpider(scrapy.Spider):
    name = "tripadvisor"

    restaurant_id_list = []
    page_offset = 0
    list_prev_len = 0
    list_cur_len = 0
    count = 0

    url = "https://www.tripadvisor.com/Restaurants-g293933-oa"+str(page_offset)+"-Azerbaijan.html#EATERY_LIST_CONTENTS"

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):

        items = RestaurantItem()
        divs = response.css("div._1llCuDZj")
        print("Page Count ----- >>> ", self.count)

        for div in divs:
            link = div.css('a._15_ydu6b').attrib['href']

            if link not in self.restaurant_id_list:
                items['id'] = ''
                items['name'] = link.split('-')[-2]
                items['restaurant_type'] = div.css("div._2rmp5aUK div._3d9EnJpt span._1p0FLy4t::text").get()
                try:
                    items['restaurant_price'] = div.css("div._2rmp5aUK div._3d9EnJpt span._1p0FLy4t::text").getall()[1]
                except:
                    items['restaurant_price'] = ''
                items['restaurantid_fk'] = "https://www.tripadvisor.com/"+str(link)
                items['page'] = self.count
                self.restaurant_id_list.append(link)

                yield items
                yield scrapy.Request("https://www.tripadvisor.com/"+str(link), self.parse_restaurants)

        self.page_offset+=30
        self.count += 1

        if self.page_offset < 61:
            next_page = "https://www.tripadvisor.com/Restaurants-g293933-oa"+str(self.page_offset)+"-Azerbaijan.html#EATERY_LIST_CONTENTS"
            yield scrapy.Request(next_page, self.parse)

    def parse_restaurants(self, response):
        items = RestaurantInfoItem()
        items['id'] = response.request.url.split('-')[-2]
        items['link'] = response.request.url
        items['coordinate'] = ''#response.css("#neighborhood img::attr(src)").get()
        items['image_url'] = response.css('div.prw_rup.prw_common_basic_image.photo_widget.large.landscape img').attrib['data-lazyurl']
        try:
            items['address'] = response.css('span.restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei::text').get()
        except:
            items['address'] = ''
        try:
            items['phone_number'] =  response.css('a.restaurants-detail-top-info-TopInfo__infoCellLink--2ZRPG::text').getall()[-1]
        except:
            items['phone_number'] = ''
        try:
            items['review_count'] = response.css('a.restaurants-detail-overview-cards-RatingsOverviewCard__ratingCount--DFxkG::text').get()
        except:
            items['review_count'] = ''
        try:
            items['rate'] = response.css("span.restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl::text").get()
        except:
            items['rate'] = ''
        try:
            rates = response.css("span.restaurants-detail-overview-cards-RatingsOverviewCard__ratingBubbles--1kQYC")
        except:
            rates = ''
        try:
            items['rate_food'] = self.get_rate(rates[0].css('span span').attrib['class'])
        except:
            items['rate_food'] = ''
        try:
            items['rate_service'] = self.get_rate(rates[1].css('span span').attrib['class'])
        except:
            items['rate_service'] = ''
        try:
            items['rate_atmosphere'] = self.get_rate(rates[3].css('span span').attrib['class'])
        except:
            items['rate_atmosphere'] = ''
        try:
            items['rate_value'] = self.get_rate(rates[2].css('span span').attrib['class'])
        except:
            items['rate_value'] = ''
        items['price_range'] = ''
        items['cuisines'] = ''
        items['meals'] = ''
        items['special_diets'] = ''
        try:
            details_title = response.css('div.restaurants-detail-overview-cards-DetailsSectionOverviewCard__categoryTitle--2RJP_::text').getall()
            details_text = response.css('div.restaurants-detail-overview-cards-DetailsSectionOverviewCard__tagText--1OH6h::text').getall()
            for title,text in zip(details_title,details_text):
                items[title.replace(' ','_').lower()] = text
        except:
            pass
        yield items

    def str_to_int(self, number):
        number = number.split(',')
        num = ''
        for n in number:
            num += n
        return int(num)

    def check_empty(self, value):
        try:
            if value:
                return value.strip()
            else:
                return ''
        except:
            return ''

    def get_rate(self, rate):
        return float(rate.split('_')[-1])/10
