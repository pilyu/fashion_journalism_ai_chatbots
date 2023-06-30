import scrapy
from ..utils import clean_html_text


class TelvaEsSpider(scrapy.Spider):
    name = 'telva_es'
    allowed_domains = ['telva.com']
    start_urls = ['https://www.telva.com/moda/moda-sostenible.html']
    
    #Parse() extract links to articles
    def parse(self, response):
        article_links = response.css('.mod-item .mod-header a::attr(href)') # Link a los artículos
        yield from response.follow_all(article_links, self.parse_article) 

        #next_page is not available all the result are in the same page
            
    def parse_article(self, response):
        yield {
            'source': 'Telva',
            'country': 'Spain',
            'headline': response.css('meta[property="og:title"]::attr(content)').get().strip(), # .strip elimna los espacios de adelante y atrás
            'date': response.css('meta[name="date"]::attr(content)').get(), # .get() se utiliza para extraer el primer elemento
            'author': response.css('.ue-c-article__byline-name::text').get(),
            'lead': clean_html_text(response.css('.ue-c-article__standfirst').get()),
            'body': clean_html_text(' '.join(response.css('.ue-c-article__body p, .ue-c-article__body h2').getall())),
            'keywords': response.css('.ue-c-article__tags .ue-c-article__tags-item a::text').getall(),
        }