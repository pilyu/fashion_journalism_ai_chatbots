import locale
import scrapy
from ..utils import clean_html_text
from datetime import datetime, timedelta


def date_ordered(date):
    locale.setlocale(locale.LC_TIME, 'es_MX')
    new_date = datetime.strptime(date, '%B %d, %Y\xa0•\xa0')
    return new_date.isoformat()


class HarpersBazaarMxSpider(scrapy.Spider):
    name = 'harpersbazaar_mx'
    allowed_domains = ['harpersbazaar.mx']
    start_urls = ['https://www.harpersbazaar.mx/search?q=sostenibilidad&s=0']

    def parse(self, response):
        article_links= response.css('a.Link::attr(href)')
        
    # Toma la 'start_url'
    def parse(self, response):
        article_links = response.css('div.PagePromo-title a::attr(href)') 
        yield from response.follow_all(article_links, self.parse_article) 

        next_page = response.css('div.Pagination-nextPage a::attr(href)').get()
        if next_page:
            yield response.follow(next_page)

    def parse_article(self, response):
        yield {
            'source': 'Harper\'s Bazaar',
            'country': 'Mexico',
            'headline': response.css('h1.Page-headline::text').get().strip(),
            'date': date_ordered(response.css('div.Page-datePublished::text').get()), 
            'author': response.css('div.Page-authors a.Link::text').get(),
            'lead': response.css('meta[name="description"]::attr(content)').get(),
            'body': clean_html_text(' '.join(response.css('div.Page-articleBody h3, div.Page-articleBody p').getall())),
            'keywords': response.css('div.Page-tags a::text').getall(),
        }
        
        
        
        
        

    
    
    