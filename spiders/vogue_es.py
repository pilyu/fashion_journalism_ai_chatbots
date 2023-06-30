import scrapy
from ..utils import clean_html_text

class VogueEsSpider(scrapy.Spider):
    name = 'vogue_es'
    allowed_domains = ['vogue.es']
    start_urls = ['https://www.vogue.es/tags/vogue-365']

    # Toma la 'start_url'
    def parse(self, response):
        article_links = response.css('a.summary-item__hed-link::attr(href)') # Link a los artículos
        yield from response.follow_all(article_links, self.parse_article) 

        next_page = response.css('a[data-section-title="Ver siguiente"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page)

    def parse_article(self, response):
        yield {
            'source': 'Vogue Spain',
            'country': 'Spain',
            'headline': response.css('meta[property="og:title"]::attr(content)').get().strip(), # .strip elimna los espacios de adelante y atrás
            'date': response.css('meta[property="article:published_time"]::attr(content)').get(), # .get() se utiliza para extraer el primer elemento
            'author': response.css('meta[property="article:author"]::attr(content)').get(),
            'lead': response.css('meta[name="description"]::attr(content)').get(),
            'body': clean_html_text(response.css('.body__inner-container').get()),
            'keywords': response.css('meta[name="keywords"]::attr(content)').getall(),
        }