import scrapy
from ..utils import clean_html_text
from scrapy.linkextractors import LinkExtractor

class PaulaClSpider(scrapy.Spider):
    name = 'paula_cl'
    allowed_domains = ['latercera.com', 'google.com'] # Paula Magazine is part of the newspaper La Tercera / Copesa S.A
    start_urls = ['https://www.google.com/search?q=site%3Alatercera.com+inurl%3Alatercera.com%2Fpaula+%22moda%22+%22sustentable%22+OR+%22sostenible%22&hl=en']

    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    }

    def parse(self, response):
        article_extractor = LinkExtractor(allow_domains='latercera.com')
        article_links = article_extractor.extract_links(response)
        yield from response.follow_all(article_links, self.parse_article)

        next_page_extractor = LinkExtractor(allow_domains="www.google.com", restrict_text='Next')
        next_page = next_page_extractor.extract_links(response)
        if next_page:
            yield response.follow(next_page[0])

    def parse_article(self, response):
        yield {
            'source': 'Paula',
            'country': 'Chile',
            'headline': response.css('h1 div::text').get(), 
            'date': response.css('meta[property="article:published_time"]::attr(content)').get(), 
            'author': clean_html_text(response.css('.byline .name').get()).split(' / ')[0],
            'lead': response.css('div.titulares > p.excerpt::text').get(),
            'body': clean_html_text(' '.join(response.css('div.single-content p.paragraph::text').getall())),
            'keywords': [clean_html_text(keyword) for keyword in response.css('.list-cat-y-tags li').getall()],
        }