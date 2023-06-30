import scrapy
from ..utils import clean_html_text



class OceandriveVeSpider(scrapy.Spider):
    name = 'oceandrive_ve'
    allowed_domains = ['oceandrive.com.ve']
    start_urls = ['https://oceandrive.com.ve/?s=moda+sustentable', 'https://oceandrive.com.ve/?s=moda+sostenible']

    #Parse() extract links to articles
    def parse(self, response):
        article_links = response.css('div.post_text_inner h2.entry_title a::attr(href)') # The selector finds all a elements nested within h2 elements inside div elements with a class of post-details
        yield from response.follow_all(article_links, self.parse_article) # Parse_article() extract data from each article page, response.follow_all() send a request to each article link 

        next_page = response.css('.pagination li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page)
            
    def parse_article(self, response):
        headline = response.css('meta[property="og:title"]::attr(content)').get()
        clean_headline = headline.replace(' - Ocean Drive Venezuela', '')
        yield {
            'source': 'Ocean Drive',
            'country': 'Venezuela',
            'headline': clean_headline,
            'date': response.css('meta[property="article:published_time"]::attr(content)').get(), 
            'author': response.css('meta[name="author"]::attr(content)').get(),
            'lead': response.css('meta[property="og:description"]::attr(content)').get(),
            'body': clean_html_text(' '.join(response.css('.qode-post-text-main p, .qode-post-text-main h3').getall())), # .getall() extract all the elements
            'keywords': response.css('.qode-tags a::text').getall(),
        }
