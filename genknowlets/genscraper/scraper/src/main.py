import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import os
import pandas as pd
import re as re
import org as orga
import re
import datetime
from sty import fg, bg, ef, rs

# Calculating the execution time
begin_time = datetime.datetime.now()

#############################################################################
## Scraping strain data
#############################################################################
class BioSpider(scrapy.Spider):
    name = 'bio'

    def __init__(self, assembly_url=None, *args, **kwargs):
        super(BioSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'{assembly_url}']

    custom_settings = {'LOG_ENABLED':'False'}

    def parse(self, response):
        self.link_genome['link'] = response.xpath("//h3//a/@href").extract()
        self.link_genome['org'] = response.xpath("//em/text()").extract_first()
        current_version = response.xpath('//*[@id="maincontent"]/div/div[5]/div[1]/div[2]/div[1]/ul/li/span/a/@href').extract()
        if len(current_version) != 0: 
            current_version = response.xpath('//*[@id="summary"]/ul/li/span/a/@href').extract()
            if len(current_version) != 0: 
                self.link_genome['current_version'] = current_version


def remove_file(filepath):
    search_file = os.path.isfile(filepath)
    if search_file == True:
        os.remove(filepath)


if __name__ == "__main__":
    assembly_url=sys.argv[1]

    link_genome = {}

    # Crawler process to extract
    BioProcess = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    BioProcess.crawl(BioSpider, assembly_url = assembly_url, link_genome=link_genome)
    BioProcess.start()

    # Convert the data extracted to variables
    if len(link_genome['link']) != 0 :
        df = pd.DataFrame.from_dict(link_genome)
        df['taxonID'] = df.link.str.extract('(\d+)')
        taxid = df.iloc[0]['taxonID']
        orgName = df.values[0][1]
        orgName = orgName.replace("(", "")
        orgName = orgName.replace(")", "")
        orgName = orgName.replace(".", "")
        orgName = re.sub('\s+', '_', orgName)
    else:
        #if len(link_genome['link']) == 0:
        link = 'https://www.ncbi.nlm.nih.gov' + str(link_genome['current_version'][0])
        cmdAssemblyUpdate = "python main_update_org.py " + link
        os.system(cmdAssemblyUpdate)
        with open('../../data/staging_data/assembly_update.txt', 'r') as f:
            link_genome = f.readlines()
        df = pd.DataFrame.from_dict(link_genome)
        os.remove('../../data/staging_data/assembly_update.txt')
        taxid = re.findall(r'\d+', str(df[0][0]))
        orgName = str(df[0][1])
        orgName = re.sub('\s+', '_', orgName)
        taxid = str(taxid[0])
    

    message = bg.da_cyan + 'Start scrapping ' + ef.italic + orgName + rs.italic + ' taxonomy and genome information . . .' + bg.rs
    print('')
    print(message)
    print('')

    # scrapping data from taxonomy and genome databases
    cmdOrg = "python org.py " + taxid + " " + orgName
    os.system(cmdOrg)

    # scrapping data from GBAD
    cmdAssemblies = "python assemblies.py " + taxid
    os.system(cmdAssemblies)

    # formating the data to be converted and generate a list of the urls to collect articles data
    cmdDataFormating = "python dataformat.py"
    os.system(cmdDataFormating)

    # scrapping data from articles
    cmdCheckArticles = "python check_articles.py"
    os.system(cmdCheckArticles)
    cmdExtractArticles = "python extract_more_articles.py"
    os.system(cmdExtractArticles)
    cmdArticles = "python articles.py"
    os.system(cmdArticles)
    #message = bg.da_cyan + 'Assembly articles scrape - Done' + bg.rs
    #print('')
    #print(message)
    #print('')

    message = bg.da_cyan + 'Starting the convertion of scrapped data to nanopublications' + bg.rs
    print('')
    print(message)
    print('')
    # converting scrapped data to rdf trig format
    cmdConverting = "python ../../converter/src/main.py"
    os.system(cmdConverting)

    remove_file('../../data/staging_data/gbad/formatted_gbad_data.json')
    remove_file('../../data/staging_data/org/organism.json')
    remove_file('../../data/staging_data/articles/articles.json')
    remove_file('../../data/staging_data/articles_links.txt')
    remove_file('../../data/staging_data/check_articles.json')
    remove_file('../../data/staging_data/assembly_links.txt')
    remove_file('../../data/staging_data/assemblies.json')

    total_time = str(datetime.datetime.now() - begin_time)
    file_summary = open("../../data/script_running_summary.csv","a+")
    file_summary.write(total_time)
    file_summary.write('\n')
    file_summary.close()


    message = bg.da_cyan + 'The process of scrapping and converting the ' + ef.italic + orgName + rs.italic + ' organism has ended.' + bg.rs
    print('')
    print(message)
    print('')
    print("Total running time: " + total_time)
    print('')