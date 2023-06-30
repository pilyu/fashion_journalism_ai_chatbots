import scrapy
from ..utils import clean_html_text


class InstyleEsSpider(scrapy.Spider):
    name = 'instyle_es'
    allowed_domains = ['instyle.es']
    start_urls = ['https://www.instyle.es/buscador/?q=sostenibilidad']
    
    # Toma la 'start_url'
    def parse(self, response):
        article_links = response.css('div.search-results-articles article a::attr(href)') # Link a los artículos
        yield from response.follow_all(article_links, self.parse_article) 

        next_page = response.css('nav.page-navigation li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page)
            
    def parse_article(self, response):
        yield {
            'source': 'InStyle',
            'country': 'Spain',
            'headline': response.css('meta[property="og:title"]::attr(content)').get().strip(), # .strip elimna los espacios de adelante y atrás
            'date': response.css('meta[name="date"]::attr(content)').get(), # .get() se utiliza para extraer el primer elemento
            'author': response.css('.lnk-author::text').get(),
            'lead': response.css('meta[property="og:description"]::attr(content)').get(),
            'body': clean_html_text(' '.join(response.css('.txt p, .txt h3').getall())),
            'keywords': [keyword.strip() for keyword in response.css('.article-block-tagrelatedsimple a::text').getall()],
        }