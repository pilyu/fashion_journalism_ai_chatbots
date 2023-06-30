import scrapy
from datetime import datetime, timezone, timedelta
from ..utils import clean_html_text, parse_date


class SomosohlalaArSpider(scrapy.Spider):
    name = 'somosohlala_ar'
    allowed_domains = ['somosohlala.com.ar', 'www.somosohlala.com.ar', 'www.somosohlala.com']
    start_urls = [
        'https://www.somosohlala.com/busqueda?keywords=moda%20sustentable',
        'https://www.somosohlala.com/busqueda?keywords=moda%20sostenible',
        'https://www.somosohlala.com/busqueda?keywords=moda%20verde',
        'https://www.somosohlala.com/busqueda?keywords=moda%20etica',
        'https://www.somosohlala.com/busqueda?keywords=moda%20verde',
        'https://www.somosohlala.com/busqueda?keywords=textil',
        'https://www.somosohlala.com/busqueda?keywords=green',
    ]
    #Note: Several pages have been selected, as the magazine does not have many articles about sustainable fashion under one tag.

    #Parse() extract links to articles
    def parse(self, response):
        article_links = response.css('article a::attr(href)')
        yield from response.follow_all(article_links, self.parse_article) # Parse_article() extract data from each article page, response.follow_all() send a request to each article link 
            
    def parse_article(self, response):
        headline = response.css('meta[property="og:title"]::attr(content)').get()
        clean_headline = headline.replace(' - Ohlalá', '')
        yield {
            'source': 'Ohlalá',
            'country': 'Argentina',
            'headline': clean_headline,
            'date': datetime.strptime(response.url[-8:], '%d%m%Y').replace(tzinfo=timezone(timedelta(hours=-3))).isoformat(), 
            'author': response.css('div.creditsContainer p.chakra-text:last-child::text').get() or 'Ohlalá',
            'lead': response.css('meta[property="og:description"]::attr(content)').get(),
            'body': clean_html_text(' '.join(response.css('#main-note-body .chakra-heading, #main-note-body .defaultStyles, #main-note-body ul').getall())),
            'keywords': response.css('#main-note-body a[href^="/etiqueta/"] p::text').getall(),
        }