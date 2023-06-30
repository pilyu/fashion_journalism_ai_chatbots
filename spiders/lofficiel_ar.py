import scrapy
import json
from scrapy.http import Request
from urllib.parse import urlencode, quote
from ..utils import clean_html_text


class LofficielArSpider(scrapy.Spider):
    name = 'lofficiel_ar'
    allowed_domains = ['lofficiel.com.ar']

    def start_requests(self):
        url = 'https://j1b4sw7ssb-dsn.algolia.net/1/indexes/*/queries?'
        parameters = {
            'x-algolia-agent': 'Algolia for JavaScript (4.10.5); Browser (lite); JS Helper (3.6.1); react (17.0.2); react-instantsearch (6.12.1)',
            'x-algolia-api-key': '2d623f7cd4b700fb2e199fe97904bddb',
            'x-algolia-application-id': 'J1B4SW7SSB',
        }
        search_url = url + urlencode(parameters, quote_via=quote)

        queries = [
            'moda sustentable',
            'moda sostenible',
        ]

        for query in queries:
            search_query = {
                'requests': [
                    {
                        'indexName': 'lofficiel_argentina_index_es',
                        'params': f'query={query}&page=0&hitsPerPage=1000',
                    }
                ]
            }

            yield Request(
                search_url,
                method='POST',
                body=json.dumps(search_query),
                callback=self.parse_result,
            )

    def parse_result(self, response):
        data = json.loads(response.body)

        for result in data['results'][0]['hits']:
            article_link = f'https://www.lofficiel.com.ar/{result["category"]["slug"]}/{result["slug"]}'
            yield response.follow(article_link, self.parse_article)

    def parse_article(self, response):
        result = json.loads(response.css('script#__NEXT_DATA__::text').get())['props']['pageProps']['subscription']['initialData']['article']

        body = ''
        for postblock in result['postBlocks']:
            if 'content' in postblock:
                body += postblock['content']

        tags = [tag['title'] for tag in result['tags']]

        yield {
            'source': 'L\'Officiel',
            'country': 'Argentina',
            'headline': result['title'],
            'date': result['_firstPublishedAt'],
            'author': result['publishedAuthorName'] or 'L\'Officiel Argentina',
            'lead': clean_html_text(result['abstract'].strip()),
            'body': clean_html_text(body),
            'keywords': tags,
        }