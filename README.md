# tripadvisor_crawler
Scrapy project to crawl restaurant info from tripadvisor.com

1. Configure scrapy environment on your computer as shown in given url - https://docs.scrapy.org/en/latest/intro/tutorial.html
2. Clone the repository 
3. Then open tripadvisor.com and click 'Restaurants'. Then search for any country
4. After the search, scroll down to bottom of the page and inspect on 2nd page to take href attribute
5. Link will be in this format, https://www.tripadvisor.com/Restaurants-g293933-oa30-Azerbaijan.html#EATERY_LIST_CONTENTS
6. Take the url and paste it in tripadvisor_spider.py as shown in the code (Page offset should be concatted, be carefull)
7. Change 'desired_count_to_scrape' to the desired number (I recommend you to take at least 5 more than the result number of pages)
8. Open 'cmd'
9. Go to the project directory, where you cloned the repo
10. Type: scrapy crawl tripadvisor
10. Enter
11. As a result, all data will be collected in tripadvisor_restaurants.db in 2 tables (my crawl for hotels in Azerbaijan is given as an example in the repo)

Note: After this, crawler will run and you will see items data shown simultaneously in your terminal
