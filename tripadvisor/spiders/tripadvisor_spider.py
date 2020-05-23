import scrapy
import re, math
from scrapy.loader import ItemLoader
from tripadvisor.items import RestaurantItem, RestaurantInfoItem, RestaurantReviewItem
import sys, os
import time

class TripadvisorSpider(scrapy.Spider):
    name = "tripadvisor"

    #Using hotel ids to not scrape the same hotel page
    restaurant_id_list = []
    #search page offset
    page_offset = 0
    #review page offset
    offset = 0
    #search page number
    count = 0
    #desired search page count to scrape
    desired_count_to_scrape = 36
    #months to scrape reviews
    months = ['March','April','May']
    #Url to scrape
    url = "https://www.tripadvisor.com/Restaurants-g293933-oa"+str(page_offset)+"-Azerbaijan.html#EATERY_LIST_CONTENTS"

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse)

    '''Parse restaurants info and links from the search page'''
    def parse(self, response):
        items = RestaurantItem()
        #Takes each restaurant block from search page
        divs = response.css("div._1llCuDZj")
        print(" -----------------------Page ",self.count," --------------------------------- ")

        for div in divs:
            link = div.css('a._15_ydu6b').attrib['href']

            if link not in self.restaurant_id_list:
                items['id'] = ''
                items['name'] = link.split('-')[-2]
                items['restaurant_type'] = div.css("div._2rmp5aUK div._3d9EnJpt span._1p0FLy4t::text").get()
                try:
                    if '$' in items['restaurant_type']:
                        items['restaurant_price'] = items['restaurant_type']
                        items['restaurant_type'] = ''
                    else:
                        items['restaurant_price'] = div.css("div._2rmp5aUK div._3d9EnJpt span._1p0FLy4t::text").getall()[1]
                except:
                    items['restaurant_price'] = ''
                items['restaurantid_fk'] = "https://www.tripadvisor.com/"+str(link)
                items['page'] = self.count
                self.restaurant_id_list.append(link)

                yield items
                #Request for each Restaurant
                # time.sleep(1)
                yield scrapy.Request("https://www.tripadvisor.com/"+str(link), self.parse_restaurants)
                # fk_url = 'https://www.tripadvisor.com/'+link
                # firstDelPos = fk_url.find('Reviews')
                # secondDelPos = fk_url.find(fk_url.split('-')[4])
                # yield scrapy.Request(fk_url.replace(fk_url[firstDelPos:secondDelPos],'or0-'), self.parse_restaurant_reviews)

        self.page_offset+=30
        self.count += 1
        #Handle Pagination
        if self.count < self.desired_count_to_scrape:
            next_page = "https://www.tripadvisor.com/Restaurants-g293933-oa"+str(self.page_offset)+"-Azerbaijan.html#EATERY_LIST_CONTENTS"
            yield scrapy.Request(next_page, self.parse)

    '''Parse each restaurant's detailed info from the given link'''
    def parse_restaurants(self, response):
        items = RestaurantInfoItem()
        items['id'] = response.request.url.split('-')[-2]
        items['link'] = response.request.url
        items['coordinate'] = ''
        items['address'] = response.css('span.restaurants-detail-overview-cards-LocationOverviewCard__detailLinkText--co3ei::text').get()
        items['review_count'] = response.css('a.restaurants-detail-overview-cards-RatingsOverviewCard__ratingCount--DFxkG::text').get()
        items['rate'] = response.css("span.restaurants-detail-overview-cards-RatingsOverviewCard__overallRating--nohTl::text").get()

        try:
            items['image_url'] = response.css('div.prw_rup.prw_common_basic_image.photo_widget.large.landscape img').attrib['data-lazyurl']
        except:
            items['image_url'] = ''
        #----
        items['phone_number'] = ''
        try:
            cells = response.css('a.restaurants-detail-top-info-TopInfo__infoCellLink--2ZRPG::text').getall()
            for cell in cells:
                if '+'in cell:
                    items['phone_number'] = cell
        except:
            pass
        #----
        try:
            rates = response.css("span.restaurants-detail-overview-cards-RatingsOverviewCard__ratingBubbles--1kQYC")
        except:
            rates = ''
        #----
        try:
            items['rate_food'] = self.get_rate(rates[0].css('span span').attrib['class'])
        except:
            items['rate_food'] = ''
        #----
        try:
            items['rate_service'] = self.get_rate(rates[1].css('span span').attrib['class'])
        except:
            items['rate_service'] = ''
        #----
        try:
            items['rate_atmosphere'] = self.get_rate(rates[3].css('span span').attrib['class'])
        except:
            items['rate_atmosphere'] = ''
        #----
        try:
            items['rate_value'] = self.get_rate(rates[2].css('span span').attrib['class'])
        except:
            items['rate_value'] = ''
        #----
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
        #----
        yield items
        #Change request url format for reviews, because new request can only made for new url and reviews in different pages
        fk_url = response.request.url
        firstDelPos = fk_url.find('Reviews-')
        secondDelPos = firstDelPos+1
        yield scrapy.Request(fk_url.replace(fk_url[firstDelPos:secondDelPos],'or10-'), self.parse_restaurant_reviews)

    '''Parse hotel reviews'''
    def parse_restaurant_reviews(self,response):
        flag = 1
        item = RestaurantReviewItem()
        review_containers = response.css('div.listContainer.hide-more-mobile div.review-container')

        review_count = self.str_to_int(response.css('a.restaurants-detail-overview-cards-RatingsOverviewCard__ratingCount--DFxkG::text').get().split(' ')[0])

        fk_url = response.request.url
        firstDelPos = fk_url.find('Reviews-')
        secondDelPos = fk_url.find(fk_url.split('-')[4])

        for review_container in review_containers:
            date = review_container.css('span.ratingDate::text').get().strip()
            month = date.split(" ")[1]
            year = date.split(" ")[-1]
            if (month in self.months) and (int(year) >= 2019):
                item['name'] = review_container.css('div.info_text.pointer_cursor div::text').get()
                item['country'] = 'No country'
                item['rate'] = str(int(review_container.css('span.ui_bubble_rating').attrib['class'].split(' ')[1].split('_')[1])/10)
                item['date'] = date
                item['title'] = review_container.css('span.noQuotes::text').get()
                item['content'] = review_container.css('p.partial_entry::text').get()

                item['restaurantreview_fk'] = fk_url#.replace(fk_url[firstDelPos:secondDelPos],'')
                yield item

            else:
                flag = 0
                break

        # review_offset = int(fk_url.split('-')[4][2:])
        # review_offset += 10
        #Check for review pages to continue
        # if (review_offset <= review_count) and flag:
        #     yield scrapy.Request(fk_url.replace(fk_url[firstDelPos+3:secondDelPos],'or'+str(review_offset)), self.parse_restaurant_reviews)

    def str_to_int(self, number):
        number = number.split(',')
        num = ''
        for n in number:
            num += n
        return int(num)

    '''Checking if selector returns value or not'''
    def check_empty(self, value):
        try:
            if value:
                return value.strip()
            else:
                return ''
        except:
            return ''

    '''Get hotel rate from the link'''
    def get_rate(self, rate):
        return float(rate.split('_')[-1])/10
