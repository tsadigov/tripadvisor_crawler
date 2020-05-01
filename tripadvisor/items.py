import scrapy

class RestaurantItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    restaurant_type = scrapy.Field()
    restaurant_price = scrapy.Field()
    restaurantid_fk = scrapy.Field()
    page = scrapy.Field()

class RestaurantInfoItem(scrapy.Item):
    id = scrapy.Field()
    link = scrapy.Field()
    coordinate = scrapy.Field()
    image_url = scrapy.Field()
    address = scrapy.Field()
    phone_number = scrapy.Field()
    review_count = scrapy.Field()
    rate = scrapy.Field()
    rate_food = scrapy.Field()
    rate_service = scrapy.Field()
    rate_atmosphere = scrapy.Field()
    rate_value = scrapy.Field()
    price_range = scrapy.Field()
    cuisines = scrapy.Field()
    meals = scrapy.Field()
    special_diets = scrapy.Field()

class RestaurantReviewItem(scrapy.Item):
    # id = scrapy.Field()
    name = scrapy.Field()
    country = scrapy.Field()
    rate = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    positive_content = scrapy.Field()
    negative_content = scrapy.Field()
    restaurantreview_fk = scrapy.Field()
