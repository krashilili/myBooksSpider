import scrapy

rating_str_to_int = lambda x: {'one':1, 'two':2, 'three':3,'four':4,'five':5}.get(x.split(' ')[-1].lower())

class mySpider(scrapy.Spider):
    name = 'myBookStore'

    start_urls = ['http://books.toscrape.com']

    # parse function
    def parse(self, response):
        BASIC_URL = 'http://books.toscrape.com/'
        # parse the page that is returned by the url in
        # the start_urls

        books = response.xpath('//article[contains(@class,"product_pod")]')
        for indx, book in enumerate(books):
            book_name = book.xpath("./h3/a/@title").extract()[0]
            rating = rating_str_to_int(book.xpath("./p/@class").extract()[0])
            price = book.xpath("./div/p[@class='price_color']/text()").extract()[0]

            yield {
                'name':book_name,
                'price': price,
                'ratings': rating
            }

        # continue the parsing on the following pages
        abs_next_url = response.xpath('//ul[@class="pager"]/li[contains(@class,"next")]/a/@href').extract()[0]
        next_url = BASIC_URL + 'catalogue/{}'.format(abs_next_url) if 'catalogue' not in abs_next_url else \
                    BASIC_URL+ abs_next_url
        # recurse
        yield scrapy.Request(next_url,callback=self.parse)