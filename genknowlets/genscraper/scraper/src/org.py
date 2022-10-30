import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import pandas as pd
import re as re
import wget
import os
import json
from sty import fg, bg, ef, rs

# Class to scrape the data from NCBI Taxonomy record 
class TaxSpider(scrapy.Spider):
    name = 'org'

    def __init__(self, taxid=None, *args, **kwargs):
        super(TaxSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?mode=Info&id={taxid}']
        self.taxid = taxid

    custom_settings = {
     'LOG_ENABLED':'False'
    }

    def parse(self, response):
        self.link_tax['tax_id'] = self.taxid
        orgName = response.css('h2 a::text').extract()
        if len(orgName) == 0:
            orgName = response.xpath('//h2//text()').extract()
        # Organism name
        self.link_tax['organism_name'] = orgName
        #print(self.link_tax['organism_name'])
        # Organism type
        self.link_tax['organism_type'] = response.css('fieldset+ strong::text').extract()
        # NCBI Taxonomy URL record
        self.link_tax['url_tax'] = self.start_urls
        yield

# Class to scrape the data from NCBI Genome record
class GenSpider(scrapy.Spider):
    name = 'org'

    def __init__(self, taxid=None, *args, **kwargs):
        super(GenSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.ncbi.nlm.nih.gov/genome/?term=txid{taxid}']
        self.taxid = taxid

    custom_settings = {
        'LOG_ENABLED':'False'
     }

    def parse(self, response):
        
        # Genome URL
        link = response.css(".GenomeLineage a:nth-child(1)::text").extract()
        if len(link) == 0:
            link.append(0)
        self.link_gen['link'] = link

        # Representative genome (0 - 1)
        representative_genome = response.css('b+ a ::attr(href)').extract()
        if len(representative_genome) == 0:
            representative_genome.append(0)
        self.link_gen['representative_genome'] = representative_genome[0]

        # Assembly quantity (1 - n)      
        qnt_assemblies = response.xpath('//*[@id="maincontent"]/div/div[1]/div[2]/b[2]/text()').extract()        
        if len(qnt_assemblies) == 0:
            qnt_assemblies = "1"
        if "genome" in qnt_assemblies[0]:
            qnt_assemblies = response.xpath('//*[@id="maincontent"]/div/div[1]/div[2]/b[3]/text()').extract()
            if len(qnt_assemblies) == 0:
                qnt_assemblies = "1"
        self.link_gen['qnt_assemblies'] = qnt_assemblies

        # Description (Data holder optinal)
        description = []
        des = ", ".join(response.xpath("//*[@id='maincontent']/div/div[5]/div/div[2]/text()").extract())
        description.append(des)
        self.link_gen['description'] = description

        description_more = []
        dm = ", ".join(response.xpath("//*[@id='moredescr_56']/text()").extract())
        if len(dm) == 0:
            dm = ", ".join(response.xpath("//*[@id='moredescr_25']/text()").extract())
            if len(dm) == 0:
                dm = "."

        # Cases where the description size is bigger
        description_more.append(dm)
        self.link_gen['descriptionMore'] = description_more

        yield

if __name__ == "__main__":

    taxid=sys.argv[1]
    #taxid = 5693

    orgName=str(sys.argv[2])

    # During the tests with real NCBI data some error occur in the orgName:
    # - Aspergillus costaricensis (Name stored in NCBI)
    # - Aspergillus costaricaensis (Name stored in GBAD)
    # With that in mind we track this special case.
    if orgName == "Aspergillus_costaricensis":
        orgName = "Aspergillus_costaricaensis" # using the name of GBAD

    outputResponse = {}
    link_gen = {}
    link_tax = {}

    # Scrapping the data from NCBI Taxonomy and Genome databases
    BioProcess = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    BioProcess.crawl(TaxSpider, outputResponse=outputResponse, taxid=taxid, link_tax=link_tax)
    BioProcess.crawl(GenSpider, outputResponse=outputResponse, taxid=taxid, link_gen=link_gen)
    BioProcess.start()
    ##

    message = bg.da_cyan + 'Taxonomy and genome information scrape - Done' + bg.rs
    print('')
    print(message)
    print('')

    df_tax = pd.DataFrame.from_dict(link_tax)
    df = pd.DataFrame.from_dict(link_gen)
    
    result = pd.concat([df_tax, df], axis=1, join="inner")
    data = result.to_json(r'../../data/staging_data/org/organism.json', orient="records")

    #Get the doc about all data in GenBank
    search_file = os.path.isfile('eukaryotes.txt')
    if search_file == False:
        print("no file")
        message = bg.da_cyan + 'Collecting the assemblies URLs related to the organism . . .' + bg.rs
        print(message)
        link = 'https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/eukaryotes.txt'
        wget.download(link)

    # Transform the .txt to pandas
    dfAssemblies = pd.read_csv('eukaryotes.txt', delimiter = "\t")

    newdf = dfAssemblies[dfAssemblies['#Organism/Name'].str.replace(' ','_').str.replace('(','').str.replace(')','').str.replace('.','').str.replace("'", "").str.replace('"','').str.contains(r'\b{}'.format(orgName), regex=True, case=False)]
   
    # Include the url 'https://www.ncbi.nlm.nih.gov/assembly/' to create the start_urls
    newdf['Assembly Accession'] = 'https://www.ncbi.nlm.nih.gov/assembly/' + newdf['Assembly Accession'].astype(str)
    
    # Save in a new .txt the Assembly Accession ID (used in assemblies.py)
    newdf['Assembly Accession'].to_csv('../../data/staging_data/assembly_links.txt', header=False, index=False)