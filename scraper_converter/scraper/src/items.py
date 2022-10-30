from typing import Text
import scrapy

class AssembliesItems(scrapy.Item):
    a1 = scrapy.Field()
    a2 = scrapy.Field()
    a3 = scrapy.Field()
    a4 = scrapy.Field()
    a5 = scrapy.Field()
    a6 = scrapy.Field()
    a7 = scrapy.Field()
    a8 = scrapy.Field()
    a9 = scrapy.Field()
    a10 = scrapy.Field()
    a11 = scrapy.Field()
    a12 = scrapy.Field()
    a13 = scrapy.Field()
    a14 = scrapy.Field()
    a15 = scrapy.Field()
    a16 = scrapy.Field()
    a17 = scrapy.Field()
    a18 = scrapy.Field()
    description = scrapy.Field()
    ftp = scrapy.Field()
    articles = scrapy.Field()
    refseqftp = scrapy.Field()
    urlfail = scrapy.Field()
    pass

class NoArticlesItems(scrapy.Item):
    url = scrapy.Field()
    check_article = scrapy.Field()
    check_article = scrapy.Field()
    assembly_pubmed = scrapy.Field()
    pass

class SearchArticlesItems(scrapy.Item):
    assembly_pubmed = scrapy.Field()
    id = scrapy.Field()
    pass
    
class ArticlesItems(scrapy.Item):
    title = scrapy.Field()
    keywords = scrapy.Field()
    pmid = scrapy.Field()
    a1 = scrapy.Field()
    a2 = scrapy.Field()
    pubType = scrapy.Field()
    dateVolume = scrapy.Field()
    abstract = scrapy.Field()
    authors = scrapy.Field()
    journal = scrapy.Field()
    assembly_pubmed = scrapy.Field()
    pmid2 = scrapy.Field()
    pass