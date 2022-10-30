import scrapy
from scrapy.crawler import CrawlerProcess
from items import SearchArticlesItems
import os

class SearchMoreArticlesSpider(scrapy.Spider):

    name = 'org'
    def __init__(self, *args, **kwargs):
        super(SearchMoreArticlesSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        search_file = os.path.isfile('../../data/staging_data/articles/more_articles.txt')
        if search_file == True:
            with open("../../data/staging_data/articles/more_articles.txt", "rt") as f:
                self.start_urls = [url.strip() for url in f.readlines()]

    custom_settings = {
     'LOG_ENABLED':'False',
     'FEED_FORMAT': 'json',
     'FEED_URI': '../../data/staging_data/articles/more_articles.json',
    }

    def parse(self, response):
        items = SearchArticlesItems()
        more_art = response.xpath("//*[@id='search-results']/div[1]/div[1]/text()").extract()

        if (len(more_art) != 0) & ("\n  \n    No results were found.\n  \n" not in more_art[0]):
            all_div = response.css(".full-docsum")
            assembly_pubmed = response.xpath("//*[@id='search-results']/h1//text()").extract()
            pmid = all_div.css(".docsum-pmid::text").extract()

        items['assembly_pubmed'] = assembly_pubmed
        items['id'] = pmid

        yield items


if __name__ == "__main__":
    
    SearchArticlesProcess = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    SearchArticlesProcess.crawl(SearchMoreArticlesSpider)
    SearchArticlesProcess.start()
    
    search_file = os.path.isfile("../../data/staging_data/articles/more_articles.txt")
    if search_file == True:
        os.remove("../../data/staging_data/articles/more_articles.txt")