import scrapy
from ..utils import clean_html_text


class VistelacalleClSpider(scrapy.Spider):
    name = 'vistelacalle_cl'
    allowed_domains = ['vistelacalle.com']
    start_urls = ['https://vistelacalle.com/category/universo-de-la-moda/slow-fashion/']

    #Parse() extract links to articles
    def parse(self, response):
        article_links = response.css('article.post_item .post_title a::attr(href)')
        yield from response.follow_all(article_links, self.parse_article) 

        next_page = response.css('.nav-next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page)
            
    def parse_article(self, response):
        yield {
            'source': 'Viste La Calle',
            'country': 'Chile',
            'headline': response.css('meta[property="og:title"]::attr(content)').get().strip(),
            'date': response.css('meta[property="article:published_time"]::attr(content)').get(), 
            'author': clean_html_text(response.css('.author_title').get()) or 'Viste La Calle',
            'lead': response.css('meta[property="og:description"]::attr(content)').get(),
            'body': clean_html_text(response.css('.post_item_single .post_content').get()),
            'keywords': response.css('meta[property="article:tag"]::attr(content)').getall(),
        }