import scrapy
import re


class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/catalogue/category/books_1/index.html"]
    links = []


    def parse(self, response):
        
        containers = response.css('div.image_container')

        for container in containers:
            link = container.css('a::attr(href)').get()
            full_link = response.urljoin(link)
            self.links.append(full_link)

        next_pag = response.css('li.next a::attr(href)').get()
        if next_pag is not None:
            next_pag = response.urljoin(next_pag)
            yield response.follow(next_pag, callback=self.parse)
        else:
            for link in self.links:
                yield scrapy.Request(link, callback=self.parse_book)


    def parse_book(self, response):
        title = response.css('div.product_main h1::text').get()

        unformatted_price = response.css('p.price_color::text').get()  
        price = float(re.sub(r'[^0-9.]', '', unformatted_price))

        stock_texts = response.css('p.instock.availability::text').getall()
        stock_joined = " ".join(s.strip() for s in stock_texts if s.strip())
        m = re.search(r'(\d+)', stock_joined or "")
        stock = int(m.group(1)) if m else 0
        
        string_rating = response.css('p.star-rating').attrib['class'].split()[-1]
        rating = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}.get(string_rating, 0)

        category = response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get().lower()
        image_url = response.urljoin(response.css('div.item.active img::attr(src)').get())

        yield {
            'title': title,
            'price': price,
            'stock': stock,
            'rating': rating,
            'category': category,
            'image_url': image_url
        }
