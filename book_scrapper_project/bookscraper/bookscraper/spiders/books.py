import scrapy
from bookscraper.items import BookscraperItem

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            item = BookscraperItem()
            item['name'] = book.css('h3 a::attr(title)').get()
            item['price'] = book.css('.price_color::text').get()
            item['stock'] = book.xpath('.//p[contains(@class, "instock")]/text()').getall()[-1].strip()
            rating_class = book.css('p.star-rating').attrib['class']
            item['rating'] = rating_class.replace('star-rating', '').strip()
            yield item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
