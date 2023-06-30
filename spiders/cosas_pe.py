import scrapy
from ..utils import clean_html_text


class CosasPeSpider(scrapy.Spider):
    name = 'cosas_pe'
    allowed_domains = ['cosas.pe']
    start_urls = ['https://cosas.pe/?s=moda+sostenible']
    
    #Parse() extract links to articles
    def parse(self, response):
        article_links = response.css('div.post-details > h2 a::attr(href)') # The selector finds all a elements nested within h2 elements inside div elements with a class of post-details
        yield from response.follow_all(article_links, self.parse_article) # Parse_article() extract data from each article page, response.follow_all() send a request to each article link 

        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page:
            yield response.follow(next_page)
            
    def parse_article(self, response):
        yield {
            'source': 'Revista COSAS',
            'country': 'Peru',
            'headline': response.css('h1.post-title::text').get(), # .get() extract the first element
            'date': response.css('meta[property="article:published_time"]::attr(content)').get(), 
            'author': response.css('meta[name=author]::attr(content)').get(),
            'lead': response.css('meta[property="og:description"]::attr(content)').get(),
            'body': clean_html_text(' '.join(response.css('section.post-content h3, section.post-content p').getall())), # .getall() extract all the elements
            'keywords': response.css('div.post-tags a::text').getall(),
        }