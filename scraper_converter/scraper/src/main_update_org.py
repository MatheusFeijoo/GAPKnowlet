import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import sys

class BioSpider(scrapy.Spider):
    name = 'bio'

    def __init__(self, assemly_url=None, *args, **kwargs):
        super(BioSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'{assembly_url}']

    custom_settings = {'LOG_ENABLED':'False'}

    def parse(self, response):
        self.link_genome['link'] = response.xpath("//h3//a/@href").extract()
        self.link_genome['org'] = response.xpath("//em/text()").extract_first()

if __name__ == "__main__":
    assembly_url=sys.argv[1]
    assembly_url = assembly_url
    link_genome = {}
    BioUpdateProcess = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    BioUpdateProcess.crawl(BioSpider , assembly_url = assembly_url, link_genome = link_genome)
    BioUpdateProcess.start()
    
    with open("../../data/staging_data/assembly_update.txt", "a") as f:
        f.write(link_genome['link'][0] + '\n')
        f.write(link_genome['org'])
