import scrapy
from scrapy.crawler import CrawlerProcess
from items import AssembliesItems
import sys
import pandas as pd
import re as re
from sty import fg, bg, ef, rs


class TaxSpider(scrapy.Spider):
    name = 'org'

    def __init__(self, tx_id=None, *args, **kwargs):
        super(TaxSpider, self).__init__(*args, **kwargs)
        with open("../../data/staging_data/assembly_links.txt", "rt") as f:
            self.start_urls = [url.strip() for url in f.readlines()]
        self.tx_id = tx_id
        # To be used when testing this single .py file
        # Need to comment 'with open' lines
        #self.start_urls = [f'https://www.ncbi.nlm.nih.gov/assembly/GCF_000209065.1']
        self.teste = 0
        self.len_org = len(self.start_urls)

    custom_settings = {
         'DOWNLOAD_DELAY': 0.25,
         'FEED_FORMAT': 'json',
         'FEED_URI': '../../data/staging_data/assemblies.json',
         'LOG_ENABLED':'False',
     }

    def parse(self, response):
        items = AssembliesItems()
        self.teste += 1
        msg = str("Scrapping assembly " + str(self.teste) + " of " + str(len(self.start_urls)))
        print(msg)

        
        refseqftp = urlfail = []

        a1 = response.css("dd:nth-child(4) , dt:nth-child(3)::text").extract()
        a2 = response.css("dd:nth-child(6) , dt:nth-child(5)::text").extract()
        # BioSample: SAMN14932942
        a3 = response.css("dd:nth-child(8) , dt:nth-child(7)::text").extract()
        # BioProject: PRJNA633093
        a4 = response.css("dd:nth-child(10) , dt:nth-child(9)::text").extract()
        # Submitter: Tulane University, School of Public Health and Tropical Medicine
        a5 = response.css("dd:nth-child(12) , dt:nth-child(11)::text").extract()
        # Date: 2020/11/06
        a6 = response.css("dd:nth-child(14) , dt:nth-child(13)::text").extract()
        # Assembly type: unresolved-diploid
        a7 = response.css("dd:nth-child(16) , dt:nth-child(15)::text").extract()
        # Assembly level: Scaffold
        a8 = response.css("dd:nth-child(18) , dt:nth-child(17)::text").extract()
        # Genome representation: full
        a9 = response.css("dd:nth-child(20) , dt:nth-child(19)::text").extract()
        # GenBank assembly accession: GCA_015455285.1 (latest)
        a10 = response.css("dd:nth-child(22) , dt:nth-child(21)::text").extract()
        # RefSeq assembly accession: n/a
        a11 = response.css("dd:nth-child(24) , dt:nth-child(23)::text").extract()
        # RefSeq assembly and GenBank assembly identical: n/a
        a12 = response.css("dd:nth-child(26) , dt:nth-child(25)::text").extract()
        # WGS Project: JACCJE01
        a13 = response.css("dd:nth-child(28) , dt:nth-child(27)::text").extract()
        # Assembly method: Geneious v. 11
        a14 = response.css("dd:nth-child(30) , dt:nth-child(29)::text").extract()
        # Expected final version: yes
        a15 = response.css("dd:nth-child(32) , dt:nth-child(31)::text").extract()
        # Reference guided assembly: GCA_003177095.1
        a16 = response.css("dd:nth-child(34) , dt:nth-child(33)::text").extract()
        # Genome coverage: 180.0x
        a17 = response.css("dd:nth-child(36) , dt:nth-child(35)::text").extract()
        # Sequencing technology: Illumina NextSeq
        a18 = response.css("dd:nth-child(38) , dt:nth-child(37)::text").extract()
        
        ftp = response.xpath("//li[(((count(preceding-sibling::*) + 1) = 5) and parent::*)]//a[contains(@href,'ftp.ncbi.nlm.nih.gov/genomes/all/GCA/')]/@href").extract()
        if len(ftp) == 0:
            ftp = response.xpath("//li[(((count(preceding-sibling::*) + 1) = 7) and parent::*)]//a[contains(@href,'ftp.ncbi.nlm.nih.gov/genomes/all/GCA/')]/@href").extract()
            if len(ftp) == 0:
                ftp = response.xpath("//li[(((count(preceding-sibling::*) + 1) = 3) and parent::*)]//a[contains(@href,'ftp.ncbi.nlm.nih.gov/genomes/all/GCA/')]/@href").extract()
                if len(ftp) == 0:
                    ftp = response.xpath("//li[(((count(preceding-sibling::*) + 1) = 6) and parent::*)]//a[contains(@href,'ftp.ncbi.nlm.nih.gov/genomes/all/GCA/')]/@href").extract()
                    if len(ftp) == 0:
                        ftp = response.xpath("//li[(((count(preceding-sibling::*) + 1) = 8) and parent::*)]//a[contains(@href,'ftp.ncbi.nlm.nih.gov/genomes/all/GCA/')]/@href").extract()
                        if len(ftp) == 0:
                            ftp = response.xpath("//li[(((count(preceding-sibling::*) + 1) = 9) and parent::*)]//a[contains(@href,'ftp.ncbi.nlm.nih.gov/genomes/all/GCA/')]/@href").extract()
        # if len(vftp) != 0:
        #     ftp = vftp
        # #print(len(a18))

        refseq = response.xpath("//li[(((count(preceding-sibling::*) + 1) = 6) and parent::*)]//a[contains(@href,'ftp.ncbi.nlm.nih.gov/genomes/all/GCF/')]/@href").extract()
        if len(refseq) == 0:
            refseq = response.xpath("//li[(((count(preceding-sibling::*) + 1) = 5) and parent::*)]//a[contains(@href,'ftp.ncbi.nlm.nih.gov/genomes/all/GCF/')]/@href").extract()
            if len(refseq) == 0:
                refseq = response.xpath("//li[(((count(preceding-sibling::*) + 1) = 7) and parent::*)]//a[contains(@href,'ftp.ncbi.nlm.nih.gov/genomes/all/GCF/')]/@href").extract()
                if len(refseq) == 0:
                    refseq = response.xpath("//li[(((count(preceding-sibling::*) + 1) = 8) and parent::*)]//a[contains(@href,'ftp.ncbi.nlm.nih.gov/genomes/all/GCF/')]/@href").extract()
        if len(refseq) != 0:
            refseqftp = refseq
        
        if len(ftp) == 0:
            urlfail.append(response.url)

        articles = response.xpath("//*[@id='summary']/p/span[2]/text()").extract()

        description = response.xpath("//*[@id='asm_comment_cont']/pre/text()").extract()
        if len(description) == 1:
            if len(description[0]) == 1:
                description = response.xpath("//*[@id='asm_comment_cont']/pre/span[1]/text()").extract()


        items['a1'] = a1
        items['a2'] = a2
        items['a3'] = a3
        items['a4'] = a4
        items['a5'] = a5
        items['a6'] = a6
        items['a7'] = a7
        items['a8'] = a8
        items['a9'] = a9
        items['a10'] = a10
        items['a11'] = a11
        items['a12'] = a12
        items['a13'] = a13
        items['a14'] = a14
        items['a15'] = a15
        items['a16'] = a16
        items['a17'] = a17
        items['a18'] = a18
        items['description'] = description
        items['ftp'] = ftp
        items['articles'] = articles
        items['refseqftp'] = refseqftp
        items['urlfail'] = urlfail

        yield items

if __name__ == "__main__":

    tx_id=sys.argv[1]
    #tx_id = 5693
    #tx_id = 3880
    outputResponse = {}
    link_genome = {}

    message = bg.da_cyan + 'Start scrapping information from the Assembly Database. . .' + bg.rs
    print('')
    print(message)
    print('')

    BioProcess = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    })
    BioProcess.crawl(TaxSpider, outputResponse=outputResponse, tx_id=tx_id, link_genome=link_genome)
    BioProcess.start()

    message = bg.da_cyan + 'Assembly Database scrape - done' + bg.rs
    print('')
    print(message)
    print('')
