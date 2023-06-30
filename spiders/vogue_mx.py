import scrapy
from ..utils import clean_html_text

class VogueMxSpider(scrapy.Spider):
    name = 'vogue_mx'
    allowed_domains = ['vogue.mx']
    start_urls = ['https://vogue.mx/sustentabilidad']

    # Toma la 'start_url'
    def parse(self, response):
        article_links = response.css('div.summary-item__content a::attr(href)') # Link a los artículos
        yield from response.follow_all(article_links, self.parse_article) 

        next_page = response.css('a.button::attr(href)').get()
        if next_page:
            yield response.follow(next_page)

    def parse_article(self, response):
        yield {
            'source': 'Vogue Mexico',
            'country': 'Mexico',
            'headline': response.css('h1::text').get().strip(), # .strip elimna los espacios de adelante y atrás
            'date': response.css('time::attr(datetime)').get(), # .get() se utiliza para extraer el primer elemento
            'author': response.css('p.byline a::text').get(),
            'lead': response.css('h1 + div::text').get(),
            'body': clean_html_text(' '.join(response.css('.article__body h2, .article__body .heading-h3, .article__body p').getall())),
            'keywords': response.css('div[data-testid="TagCloudWrapper"] a span::text').getall(),
        }