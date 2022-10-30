import scrapy
from scrapy.crawler import CrawlerProcess
from items import NoArticlesItems
import pandas as pd
import os
from sty import fg, bg, ef, rs

class NoArticlesSpider(scrapy.Spider):

    name = 'org'
    def __init__(self, *args, **kwargs):
        super(NoArticlesSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        search_file = os.path.isfile('../../data/staging_data/articles_links.txt')
        if search_file == True:
            with open("../../data/staging_data/articles_links.txt", "rt") as f:
                self.start_urls = [url.strip() for url in f.readlines()]
            self.articles = len(self.start_urls)
            self.count = 0
            print(' ')

    custom_settings = {
     'LOG_ENABLED':'False',
     'FEED_FORMAT': 'json',
     'FEED_URI': '../../data/staging_data/check_articles.json',
     'DOWNLOAD_DELAY': 0.25,
    }

    def parse(self, response):
        items = NoArticlesItems()
        self.count += 1
        msg = str("Searching articles for the " + str(self.count) + '° assembly.')
        print(msg)
        url = response.url
        check_article = response.xpath('//*[@id="search-results"]/div[1]/div[1]//text()').extract()
        assembly_pubmed = response.xpath('//*[@id="article-top-actions-bar"]/div/div/div[1]/span/span//text()').extract()
        items['check_article'] = len(check_article)
        items['url'] = url
        items['assembly_pubmed'] = assembly_pubmed

        yield items

if __name__ == "__main__":
    
    
    message = bg.da_cyan + 'Starting scraping assembly articles ...' + bg.rs
    print('')
    print(message)
    print('')

    SearchArticlesProcess = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    SearchArticlesProcess.crawl(NoArticlesSpider)
    SearchArticlesProcess.start()

    df_json = pd.read_json('../../data/staging_data/check_articles.json')
    df = pd.DataFrame(df_json.values.tolist())
    one = 0
    more = 0
    df_one_article = pd.DataFrame(columns=['pubmed_assembly', 'id'])
    
    for i in range(0, len(df)):
        
        if len(df[2][i]) != 0:
            if df[0][i] == 0:
                #print("-------")
                #print(df[2][i][0])
                df[1][i] = df[1][i].replace("https://pubmed.ncbi.nlm.nih.gov/", "")
                df[1][i] = df[1][i].replace("/", "")
                pubmed_assembly = []
                pubmed_assembly.append([str(df[2][i][0])])
                id = []
                id.append([str(df[1][i])])
                df_one_article.loc[0 if pd.isnull(df_one_article.index.max()) else df_one_article.index.max() + 1] = pubmed_assembly + id
                one += 1
        
        if df[0][i] == 4:
            with open("../../data/staging_data/articles/more_articles.txt", "a") as f:
                f.write((df[1][i]) + "\n")
            more += 1

    print(' ')
    print(' ')
    message_one = bg.da_cyan + str(one) + " assemblies have one article citing them." + bg.rs
    message_more = bg.da_cyan + str(more) + " assemblies have more than one article citing them." + bg.rs
    print(message_one)
    print(message_more)
    print(' ')
    print(' ')
    data = df_one_article.to_json(r'../../data/staging_data/articles/one_article.json', orient="records")
    #os.remove("../../data/staging_data/check_articles.json")
    #os.remove("../../data/staging_data/articles_links.txt")