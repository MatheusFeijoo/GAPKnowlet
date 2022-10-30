import rdflib 
from rdflib.graph import Dataset
from rdflib.namespace import DCTERMS, RDF
from rdflib.term import URIRef
import sys
import os
import wget
import pandas as pd
import datetime
import hashlib
from random import random
import knowlet_constants as knowlet_cnt
pd.options.mode.chained_assignment = None


## Create knowlet using genscraper outputs
def create_knowlet_genknowlet():
    print(' ')
    print('** The .trig files need to be on the knowlet/input directory **')
    print(' ')
    org_name = input('Enter the already extracted genus organism name: ')
    ##### Collecting all the taxid to be insert in a knowlet organism
    org_name = org_name.replace(' ', '')
    org_name = org_name.lower() + ' '
    search_file = os.path.isfile('eukaryotes.txt')
    if search_file == False:
        link = 'https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/eukaryotes.txt'
        wget.download(link)
    file = pd.read_csv('eukaryotes.txt', delimiter = "\t")
    file.sort_values('#Organism/Name', inplace = True)
    file['#Organism/Name'] = file['#Organism/Name'].str.lower()
    right_org = file.loc[file['#Organism/Name'].str.contains(org_name, case=False)]
    right_org.drop_duplicates(subset ='TaxID',keep = 'first', inplace = True)
    new = right_org['#Organism/Name'].str.split(' ', n = 2, expand = True)
    right_org["genus"] = new[0]
    right_org["repeat"] = new[1]
    right_org.drop_duplicates(subset ='repeat',keep = 'first', inplace = True)
    org_name = org_name.replace(' ', '')
    right_org = right_org[right_org['genus'] == org_name]    
    right_org = right_org.reset_index(drop=True)   
    npub_id_triple = []
    #####
    ##### Collecting id from the organism/gbad/article nanopubs
    # npub_id_triple = []
    # org = Dataset()
    # org.parse('input/organism.trig')
    # org_npub_id = []
    # npub_id_triple.append("\n")
    # #print(len(right_org['TaxID']))
    # for i in range (0, len(right_org['TaxID'])):
    #     url = right_org['TaxID'][i]
    #     org_result = org.query ("""
    #     SELECT ?np
    #     WHERE {
    #         GRAPH ?head{
    #             ?np np:hasProvenance ?provenance .
    #             ?np np:hasAssertion ?assertion .
    #         }
    #         GRAPH ?assertion{
    #             ?taxid foaf:name ?name .
    #             filter contains(?teste, "Acremonium")
    #         }
    #     }""" % url)
    #     print(org_result[0])
    #     for row in org_result:
    #         org_npub_id.append(str(row[0]))
    #     print(len(org_npub_id))
    #     npub_id_triple.append("    ro:0001018 <" + org_npub_id[i] + "> ;\n")

    # print(' ')
    # print('Found ' + str(len(org_npub_id)) + ' organism nanopubs citing the organism')
    # gbad = Dataset()
    # gbad.parse('input/gbad.trig')
    # gbad_npub_id = []
    # for i in range (0, len(org_npub_id)):
    #     url = org_npub_id[i]
    #     gbad_result = gbad.query ("""
    #     SELECT ?np
    #     WHERE {
    #         GRAPH ?head{
    #             ?np np:hasAssertion ?assertion .
    #         }
    #         GRAPH ?assertion{
    #             <%s> sio:SIO_000628 sio:SIO_010000 .
    #         }
    #     }""" % url)
    #     for row in gbad_result:
    #         gbad_npub_id.append(str(row[0]))
    #         npub_id_triple.append("    ro:0001018 <" + gbad_npub_id[i] + "> ;\n")

    # print('Found ' + str(len(gbad_npub_id)) + ' gbad nanopubs citing the organism')
    # articles = Dataset()
    # articles.parse('input/articles.trig')
    # articles_npub_id = []
    # for i in range (0, len(gbad_npub_id)):
    #     url = gbad_npub_id[i]
    #     articles_result = articles.query ("""
    #     SELECT ?np
    #     WHERE {
    #         GRAPH ?head{
    #             ?np np:hasAssertion ?assertion .
    #         }
    #         GRAPH ?assertion{
    #             ?subOrg data:usesIdentifierScheme np:Nanopublication .
    #             ?subOrg prov:value <%s> .
    #         }
    #     }""" % url)
    #     for row in articles_result:
    #         articles_npub_id.append(str(row[0]))
    # for i in range (0, len(articles_npub_id)):        
    #     npub_id_triple.append("    ro:0001018 <" + articles_npub_id[i] + "> ;\n")
    # print('Found ' + str(len(articles_npub_id)) + ' article nanopubs citing the organism')
    # print(' ')
    # print(' ')
    #####
    ##### Collecting additional nanopublications
    print('To insert other nanopublications to the knowlet, they must be in the input/other_npub.txt file ')
    answer_add_npubs = input('Wants to insert other nanopubs related to ' + org_name + ' to the knowlet ? (Y: yes / N: no) ')
    if answer_add_npubs == 'y' or answer_add_npubs == 'Y' or answer_add_npubs == 'yes':
        print(' ')
        for retry in range(2):
            other_file = os.path.isfile('input/other_npub.txt')
            if other_file == True:
                with open('input/other_npub.txt') as f:
                    other_np_related = f.readlines()
                break
            print('Warning:')
            check_other = input('The nanopublications related to organism are in the input/other_npub.txt file ?')
    #####
    ##### Conversion of the npubs to triples format
    if len(other_np_related) != 0:
        for i in range (0, len(other_np_related)):
            other_np_related[i] = other_np_related[i].replace('\n','')
            npub_id_triple.append("   ro:0001018 <" + other_np_related[i] + "> ;\n")
    npub_id_triple[-1] = npub_id_triple[-1].replace(';', '.') 
    npub_id_triple = ' '.join(npub_id_triple)
    #####
    ##### Insertion of keywords for provenance
    print(' ')
    keywords = input('Insert the keywords related to the knowlet: (delimited by ", ") ')
    keywords = keywords.replace(',', '"@en, "')
    keywords = '"' + keywords + '.'
    #####
    ##### Creation of the hash for the npub
    hash = hash_creation(org_name)
    ##### Time variables
    np_date = date()
    np_year = np_date[0]
    np_month = np_date[1]
    np_day = np_date[2]
    #####
    ##### Creators
    # print(' ')
    # creators = input('Insert the creators ORCID of this knowlet: (delimited by ", ") ')
    # creators = creators.replace(', ', '>, <')
    # #####
    # ##### Creators Institution
    # print(' ')
    # institution = input('Insert the institution(s) related to the creators: (delimited by ", ")')
    #####
    ##### Knowlet Curators
    # curators = input('Insert the curators ORCID of this knowlet: (delimited by ", ") ')
    # curators = curators.replace(', ', '>, <')
    ##### Knowlet Creation
    knowlet_prefixs = knowlet_cnt.prefixes.format(hash = hash)
    knowlet_head = knowlet_cnt.head
    knowlet_assertion = knowlet_cnt.assertion.format(
        other_knowlet = ' ', subject = org_name, nanopubs = npub_id_triple, other_knowlet_full = ' '
    )
    knowlet_prov = knowlet_cnt.provenance.format(
        current_version = '1.0', revision = '', dayprov = np_day, monthprov = np_month,
        yearprov = np_year
    )
    knowlet_pubinfo = knowlet_cnt.pubinfo.format(
        keywords = keywords, daynp = np_day, monthnp = np_month, yearnp = np_year
    )

    knowlet = knowlet_prefixs + "\n" + knowlet_head + "\n"
    knowlet += knowlet_assertion + "\n" + knowlet_prov + "\n"
    knowlet += knowlet_pubinfo
    file = str("output/knowlet_" + org_name + ".trig")
    with open(file, "w") as f:
        f.write(knowlet)
        f.close()
    print('change write to append.')

## Creating a normal knowlet
def create_knowlet():
    subject = input('Insert the subject related to the knowlet: ')
    npub_id_triple = []
    npub_id_triple.append('\n')
    file = os.path.isfile('input/other_npub.txt')
    if file == True:
        with open('input/other_npub.txt') as f:
            np_related = f.readlines()
    
    if len(np_related) != 0:
        for i in range (0, len(np_related)):
            np_related[i] = np_related[i].replace('\n','')
            npub_id_triple.append("    ro:0001018 <" + np_related[i] + "> ;\n")
    npub_id_triple[-1] = npub_id_triple[-1].replace(';', '.') 
    npub_id_triple = ' '.join(npub_id_triple)
    #####
    ##### Insertion of keywords for provenance
    print(' ')
    keywords = input('Insert the keywords related to the knowlet: (delimited by ", ") ')
    keywords = keywords.replace(',', '"@en, "')
    keywords = '"' + keywords + '.'
    #####
    ##### Creation of the hash for the npub
    hash = hash_creation(keywords[0])
    ##### Time variables
    np_date = date()
    np_year = np_date[0]
    np_month = np_date[1]
    np_day = np_date[2]
    #####
    ##### Creators
    print(' ')
    creators = input('Insert the creators ORCID of this knowlet: (delimited by ", ") ')
    creators = creators.replace(', ', '>, <')
    #####
    ##### Creators Instituion
    print(' ')
    institution = input('Insert the institution(s) related to the creators: (delimited by ", ")')
    #####
    ##### Knowlet Curators
    curators = input('Insert the curators ORCID of this knowlet: (delimited by ", ") ')
    curators = curators.replace(', ', '>, <')
    ##### Knowlet Creation
    knowlet_prefixs = knowlet_cnt.prefixes.format(hash = hash)
    knowlet_head = knowlet_cnt.head
    knowlet_assertion = knowlet_cnt.assertion.format(
        other_knowlet = ' ', subject = subject, nanopubs = npub_id_triple, other_knowlet_full = ' '
    )
    knowlet_prov = knowlet_cnt.provenance.format(
        current_version = '1.0', revision = '', dayprov = np_day, monthprov = np_month,
        yearprov = np_year, creators = creators, creator_inst = institution
    )
    knowlet_pubinfo = knowlet_cnt.pubinfo.format(
        keywords = keywords, daynp = np_day, monthnp = np_month, yearnp = np_year,
        curators = curators
    )

    knowlet = knowlet_prefixs + "\n" + knowlet_head + "\n"
    knowlet += knowlet_assertion + "\n" + knowlet_prov + "\n"
    knowlet += knowlet_pubinfo
    with open("output/knowlet.trig", "w") as f:
        f.write(knowlet)
        f.close()
    print('change write to append.')

def hash_creation(str_hash):
    hash = (str(str_hash) + str(random()))
    hash = hash.encode()
    hash = hashlib.md5(hash).hexdigest()
    return hash

def date():
    date= pd.to_datetime(datetime.datetime.now(),format='%Y-%m-%d')
    np_day = pd.to_datetime(date).day
    np_month = pd.to_datetime(date).month
    np_year = pd.to_datetime(date).year
    np_date = []
    np_date.append(np_year)
    np_date.append(np_month)
    np_date.append(np_day)
    return np_date

if __name__ == "__main__":
    #mode = sys.argv[1]
    #knowlet_id = sys.argv[2]
    
    #if mode == 'create':
        # Choose if the created knowlet will start about the genscraper output
    knowlet_type = input('Wants to create a new knowlet based on genscraper organism? (Y: yes / N: no) ')
    if knowlet_type == 'Y' or knowlet_type == 'y' or knowlet_type == 'yes':
        create_knowlet_genknowlet()
    if knowlet_type == 'N' or knowlet_type == 'n' or knowlet_type == 'no':
        create_knowlet()
    
    
    #if mode == 'update':

    # KNOWLET UPDATE:
    # change version(revision) 
    #   {current_version} 
    #   {revision} -    prov:wasRevisionOf "1.1"@en ;
    # insert/delete npubs
    # other knowlets related 
    #   {other_knowlet} -    dc:relation sub:OtherKnowlet ;
    #   {other_knowlet_full} -    sub:OtherKnowlet a prov:collection;
    #                             prov:hadPrimarySource <link>;
    #                             obi:OBI_0200113 <result>; #conceptual similarity result
