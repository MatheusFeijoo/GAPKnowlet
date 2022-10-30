import scrapy
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from items import ArticlesItems
from sty import fg, bg, ef, rs
pd.options.mode.chained_assignment = None

### More articles
class MoreArticlesSpider(scrapy.Spider):
    name = 'org'

    def __init__(self, *args, **kwargs):
        super(MoreArticlesSpider, self).__init__(*args, **kwargs)
        self.start_urls = []     
        search_file = os.path.isfile('../../data/staging_data/articles/more_articles.json')
        empty_file = os.stat('../../data/staging_data/articles/more_articles.json').st_size
        if search_file == True and empty_file != 0:
            with open(f'../../data/staging_data/articles/more_articles.json') as f_in: 
                data = json.load(f_in)
            for i in range(0, len(data)):    
                for j in range(0, len(data[i]["id"])):
                    self.start_urls.append(f'https://pubmed.ncbi.nlm.nih.gov/{data[i]["id"][j]}/')
        

    custom_settings = {
     'LOG_ENABLED':'False',
     'FEED_FORMAT': 'json',
     'FEED_URI': '../../data/staging_data/articles/more_articles_extracted.json',
    }

    def parse(self, response):
        items = ArticlesItems()
        title = ''
        keywords = ''
        pmid = ''
        a1 = ''
        a2 = ''
        pubType = ''
        dateVolume = ''
        abstract = ''
        authors = ''
        journal = ''

        title = ", ".join(response.xpath('normalize-space(//*[@id="full-view-heading"]/h1)').extract())
        keywords = response.xpath('//*[@id="abstract"]/p/text()').extract()
        if len(keywords) != 0:
            keywords = list( dict.fromkeys(keywords) )
            keywords.remove("\n      \n        ")
        pmid = response.xpath('//*[@id="full-view-identifiers"]/li[1]/span/strong/text()').extract()
        a1 = response.xpath('normalize-space(//*[@id="full-view-identifiers"]/li[2]/span/a/@href)').extract()
        a2 = response.xpath('normalize-space(//*[@id="full-view-identifiers"]/li[3]/span/a/@href)').extract()
        pubType = response.xpath('normalize-space(//*[@id="full-view-heading"]/div[1]/div[1]//text())').extract()
        dateVolume = response.xpath('normalize-space(//*[@id="full-view-heading"]/div[1]/div/span[2])').extract()
        abstract = response.xpath('normalize-space(//*[@id="enc-abstract"]/p)').extract()
        authors = response.xpath('//*[@id="full-view-heading"]/div[2]/div/div//text()').extract()
        ## formatting the authors
        authors = list( dict.fromkeys(authors) )
        authors.remove("\n    ")
        authors.remove(",\xa0")
        authors.remove("\xa0")
        authors.remove("\n  ")
        authors.remove("\n                1\n              ")
        ##
        journal = response.xpath('normalize-space(//*[@id="full-view-journal-trigger"]//text())').extract()

        assembly_pubmed = "txt"

        items['title'] = title
        items['keywords'] = keywords
        items['pmid'] = pmid
        items['a1'] = a1
        items['a2'] = a2
        items['pubType'] = pubType
        items['dateVolume'] = dateVolume
        items['abstract'] = abstract
        items['authors'] = authors
        items['journal'] = journal
        items['assembly_pubmed'] = assembly_pubmed
        items['pmid2'] = pmid


        yield items


###One article
class OneArticleSpider(scrapy.Spider):

    name = 'org'
    def __init__(self, *args, **kwargs):
        super(OneArticleSpider, self).__init__(*args, **kwargs)
        self.start_urls = []     
        search_file = os.path.isfile('../../data/staging_data/articles/one_article.json')
        if search_file == True:
            with open(f'../../data/staging_data/articles/one_article.json') as f_in:
                data = json.load(f_in)
            for i in range(0, len(data)):
                for j in range(0, len(data[i]["id"])):
                    self.start_urls.append(f'https://pubmed.ncbi.nlm.nih.gov/{data[i]["id"][j]}/')

    custom_settings = {
     'LOG_ENABLED':'False',
     'FEED_FORMAT': 'json',
     'FEED_URI': '../../data/staging_data/articles/one_article_extracted.json',
     'DOWNLOAD_DELAY': 0.25,
    }

    def parse(self, response):
        items = ArticlesItems()
        title = ''
        keywords = ''
        pmid = ''
        a1 = ''
        a2 = ''
        pubType = ''
        dateVolume = ''
        abstract = ''
        authors = ''
        journal = ''

        title = ", ".join(response.xpath('normalize-space(//*[@id="full-view-heading"]/h1)').extract())
        keywords = response.xpath('//*[@id="abstract"]/p/text()').extract()
        if len(keywords) != 0:
            keywords = list( dict.fromkeys(keywords) )
            keywords.remove("\n      \n        ")
        pmid = response.xpath('//*[@id="full-view-identifiers"]/li[1]/span/strong/text()').extract()
        a1 = response.xpath('normalize-space(//*[@id="full-view-identifiers"]/li[2]/span/a/@href)').extract()
        a2 = response.xpath('normalize-space(//*[@id="full-view-identifiers"]/li[3]/span/a/@href)').extract()
        pubType = response.xpath('//*[@id="full-view-heading"]/div[1]/div[1]//text()').extract()
        dateVolume = response.xpath('normalize-space(//*[@id="full-view-heading"]/div[1]/div/span[2])').extract()
        abstract = response.xpath('normalize-space(//*[@id="enc-abstract"]/p)').extract()
        authors = response.xpath('//*[@id="full-view-heading"]/div[2]/div/div//text()').extract()
        ## formatting the authors
        authors = list( dict.fromkeys(authors) )
        authors.remove("\n    ")
        authors.remove(",\xa0")
        authors.remove("\xa0")
        authors.remove("\n  ")
        ##
        journal = response.xpath('normalize-space(//*[@id="full-view-journal-trigger"]//text())').extract()
        assembly_pubmed = "txt"

        items['title'] = title
        items['keywords'] = keywords
        items['pmid'] = pmid
        items['a1'] = a1
        items['a2'] = a2
        items['pubType'] = pubType
        items['dateVolume'] = dateVolume
        items['abstract'] = abstract
        items['authors'] = authors
        items['journal'] = journal
        items['assembly_pubmed'] = assembly_pubmed
        items['pmid2'] = pmid


        yield items
###





def formatting_articles(link, file):

    df_json = pd.read_json(f'../../data/staging_data/articles/{file}.json')
    df = pd.DataFrame(df_json.values.tolist())
    df_links_json = pd.read_json(f'../../data/staging_data/articles/{link}.json')
    df_links = pd.DataFrame(df_links_json.values.tolist())
    
    for i in range(0, len(df_links)):
        df_links[0][i][0] = df_links[0][i][0].replace("PubMed for id: ", "") 
    
    if file == "more_articles_extracted":
        for i in range(0, len(df[2])):
            for j in range (0, len(df_links[1])):
                    for a in range (0, len(df_links[1][j])):
                        if df[2][i][0] == df_links[1][j][a] and df_links[0][j] != '':
                            df[10][i] = df_links[0][j]

    if file == "one_article_extracted":
        for i in range(0, len(df[2])):
            for j in range (0, len(df_links[1])):
                # print("-----------------")
                # print(df_links[0][j])
                # print(df[2][i][0])
                if df[2][i][0] == df_links[1][j][0]:
                    df[10][i] = df_links[0][j]
                    df_links[1][j][0] = ''
                    df[2][i][0] = ''
    return(df)

def save_articles(df_one, test_one, df_more, test_more):
    
    if test_one != 0 and test_more != 0:
        frames = [df_one, df_more]
        all_articles = pd.concat(frames, ignore_index=True)
        data = all_articles.to_json(r'../../data/staging_data/articles/articles.json', orient="records")

    if test_one == 0 and test_more != 0:
        data = df_more.to_json(r'../../data/staging_data/articles/articles.json', orient="records")
    if test_one != 0 and test_more == 0:
        data = df_one.to_json(r'../../data/staging_data/articles/articles.json', orient="records")
    if test_one == 0 and test_more == 0:
        print("no articles")

def removing_file(file):
    search_file = os.path.isfile(file)
    if search_file == True:
        os.remove(file)




if __name__ == "__main__":

    ArticlesProcess = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    ArticlesProcess.crawl(MoreArticlesSpider)
    ArticlesProcess.crawl(OneArticleSpider)
    ArticlesProcess.start()

    connection_more = "more_articles"
    more_file = "more_articles_extracted"
    connection_one = "one_article"
    one_file = "one_article_extracted"
    
    df_more = 0
    test_more = 0
    search_file = os.path.isfile('../../data/staging_data/articles/more_articles_extracted.json')
    if search_file == True:
        test_more = os.stat('../../data/staging_data/articles/more_articles_extracted.json').st_size
        if test_more != 0:
            df_more = formatting_articles(connection_more, more_file)
    
    df_one = 0
    test_one = 0
    search_file = os.path.isfile('../../data/staging_data/articles/one_article_extracted.json')
    if search_file == True:
        test_one = os.stat('../../data/staging_data/articles/one_article_extracted.json').st_size
        if test_one != 0:
            df_one = formatting_articles(connection_one, one_file)
    
    save_articles(df_one, test_one, df_more, test_more)
    
    removing_file('../../data/staging_data/articles/more_articles_extracted.json')
    removing_file('../../data/staging_data/articles/more_articles.json')
    removing_file('../../data/staging_data/articles/one_article_extracted.json')
    removing_file('../../data/staging_data/articles/one_article.json')