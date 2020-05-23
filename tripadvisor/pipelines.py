import sqlite3
from .items import RestaurantItem, RestaurantInfoItem, RestaurantReviewItem

class TripadvisorPipeline(object):
    def __init__(self):
            self.create_connection()
            self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("tripadvisor_restaurants.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS restaurant_table""")
        self.curr.execute("""DROP TABLE IF EXISTS restaurant_info_table""")
        self.curr.execute("""DROP TABLE IF EXISTS restaurant_review_table""")
        self.curr.execute("""create table restaurant_table(
                    id text,
                    name text,
                    restaurant_type text,
                    restaurant_price text,
                    restaurantid_fk text,
                    page text
                    )""")
        self.curr.execute("""create table restaurant_info_table(
                    id text,
                    link text,
                    coordinate text,
                    image_url text,
                    address text,
                    phone_number text,
                    review_count text,
                    rate text,
                    rate_food text,
                    rate_service text,
                    rate_atmosphere text,
                    rate_value text,
                    price_range text,
                    cuisines text,
                    meals text,
                    special_diets text
                    )""")
        self.curr.execute("""create table restaurant_review_table(
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    name text,
                    country text,
                    rate text,
                    date text,
                    title text,
                    content text,
                    restaurantreview_fk text
                    )""")

    def process_item(self, item, spider):
        if isinstance(item, RestaurantItem):
            self.store_restaurant(item)
        if isinstance(item, RestaurantInfoItem):
            self.store_restaurant_info(item)
        if isinstance(item, RestaurantReviewItem):
            self.store_restaurant_review(item)
        return item

    def store_restaurant(self, item):
        self.curr.execute("""insert into restaurant_table values (?,?,?,?,?,?)""",(
            item['id'],
            item['name'],
            item['restaurant_type'],
            item['restaurant_price'],
            item['restaurantid_fk'],
            item['page']
        ))
        self.conn.commit()

    def store_restaurant_info(self, item):
        self.curr.execute("""insert into restaurant_info_table values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
            item['id'],
            item['link'],
            item['coordinate'],
            item['image_url'],
            item['address'],
            item['phone_number'],
            item['review_count'],
            item['rate'],
            item['rate_food'],
            item['rate_service'],
            item['rate_atmosphere'],
            item['rate_value'],
            item['price_range'],
            item['cuisines'],
            item['meals'],
            item['special_diets']
        ))
        self.conn.commit()

    def store_restaurant_review(self, item):
        self.curr.execute("""insert into restaurant_review_table values (?,?,?,?,?,?,?,?)""",(
            None,
            item['name'],
            item['country'],
            item['rate'],
            item['date'],
            item['title'],
            item['content'],
            item['restaurantreview_fk'],
        ))
        self.conn.commit()
