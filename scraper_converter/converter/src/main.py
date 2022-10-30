import json
import os
import nanopub_constants_gbad as np_cnt_gbad
import nanopub_constants_article as np_cnt_art
import nanopub_constants_org as np_cnt_org
import datetime
import pandas as pd
import hashlib
from random import random
from sty import fg, bg, ef, rs
pd.options.mode.chained_assignment = None

# extract data to a dict
def extract_dict_from_file(filepath):
    readmode = "r"
    with open(filepath, readmode) as f:
        d = json.load(f)
    return d

# create all hash id
def hash_creation(str_hash):
    hash = (str(str_hash) + str(random()))
    hash = hash.encode()
    hash = hashlib.md5(hash).hexdigest()
    return hash

# date definition for the npubs
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

# identification of the curators orcid
def orcid():
    with open('../../data/staging_data/orcid.txt', 'r') as f:
        orcid = [line.strip() for line in f]
    for lines in range(len(orcid)):
        orcid[lines] = orcid[lines].replace(orcid[lines], "<"+orcid[lines]+"> , ")
    orcid[len(orcid) - 1] = orcid[len(orcid) - 1].replace(" ,", "")
    orcid = ''.join(orcid)
    return(orcid)

# organism convertiton to rdf trig format
def convert_org_dict_to_rdf(dict_input, hash_org, orcid, np_date):
    nanopubs = []
    np_year = np_date[0]
    np_month = np_date[1]
    np_day = np_date[2]
    description_org = ''
    description_total_org = ''

    #"Reference genome: "
    if dict_input[0]["qnt_assemblies"] != 0:
        qnt_assemblies = dict_input[0]["qnt_assemblies"].replace("All ", "")
        qnt_assemblies = qnt_assemblies.replace(" genomes for species:", "")
        qnt_assemblies = qnt_assemblies.replace(" ", "")

    assembly_id = dict_input[0]["tax_id"]

    # Collecting data to generate a summary of the script
    file_summary = open("../../data/script_running_summary.csv","a+")
    file_summary.write(dict_input[0]["organism_name"] + ', 1, ')
    file_summary.close

    if len(dict_input[0]["description"]) != 0 :
        dict_input[0]["description"] = dict_input[0]["description"].replace('"', "'")
        dict_input[0]["descriptionMore"] = dict_input[0]["descriptionMore"].replace('"', "'")
        description_org = '\n    ncit:C101282 sub:description ; '
        description_total_org = ('\n\n  sub:description a prov:Entity ;' +
                            '\n    rdf:type dcterms:description ;' +
                            '\n    prov:value "' + dict_input[0]["description"] + dict_input[0]["descriptionMore"] + '"@en ;'+
                            '\n    prov:wasQuotedFrom <https://www.ncbi.nlm.nih.gov/genome/?term=txid'+ dict_input[0]["tax_id"] +'> .' )
    
    np_prefixes = np_cnt_org.prefixes.format(
        hash = hash_org)
    np_head = np_cnt_org.head
    np_assertions = np_cnt_org.assertion.format(
        tax_id = assembly_id, organism_name = dict_input[0]["organism_name"],
        representative_genome = dict_input[0]["representative_genome"],
        qnt_assemblies = qnt_assemblies)
    np_prov = np_cnt_org.provenance.format(
        url_tax = dict_input[0]["url_tax"], description = description_org, tax_id = assembly_id,
        prov_day = np_day, prov_month = np_day,
        prov_year = np_year, description_total = description_total_org)
    np_pubinfo = np_cnt_org.pubinfo.format(
        url_tax = dict_input[0]["url_tax"], tax_id = assembly_id, np_day = np_day, np_month = np_month,
        np_year = np_year, orcid = orcid)

    nanopub = np_prefixes + "\n" + np_head + "\n"
    nanopub += np_assertions + "\n" + np_prov + "\n"
    nanopub += np_pubinfo
    nanopubs.append(nanopub)

    return nanopubs, True

#Converte gbad to rdf
def convert_gbad_dict_to_rdf(dict_input, hash_org, orcid, np_date):
    nanopubs = []
    genbank_accession = biosample = bioproject = infra_name = gen_representation = assembly_type = assembly_level = genome_coverage = refseq = refseq_type = refseq_url = tech = method = wgs = wgs_project_id = wgs_version = isolate = description = reference = submitter = dayprov = monthprov = yearprov = ftp = description_full = hash_gbad = refseq_url_total = ''
    org_npub = hash_org
    year_np = np_date[0]
    month_np = np_date[1]
    day_np = np_date[2]

    number_of_articles = 0
    # article dataframe executed at the same time of the related assembly
    search_file = os.path.isfile('../../data/staging_data/articles/articles.json')
    if search_file == True:
        df_articles = pd.read_json('../../data/staging_data/articles/articles.json')
        df_articles = pd.DataFrame(df_articles.values.tolist())
        number_of_articles = len(df_articles)
        for i in range (0, len(df_articles)):
            df_articles[10][i] = str(df_articles[10][i][0])


    # Collecting data to generate a summary of the script
    file_summary = open("../../data/script_running_summary.csv","a+")
    file_summary.write(str(len(dict_input)) + ', ' + str(number_of_articles) + ', ') 
    file_summary.close

    for i in range(0, (len(dict_input))):
        wgs = ''
        wgs_project_id = ''
        wgs_version = ''
        wgs_version_name = ''
        print("Converting strain assembly " + str(i+1) + " of " + str(len(dict_input)))
        #FTP - prov graph
        if len(dict_input[19][i]) != 0:
            if str(dict_input[19][i]) != "[' ']":
                ftp = dict_input[19][i][0]            

            #ARTICLE
            if len(dict_input[20][i]) != 0:
                if str(dict_input[20][i]) != "[' ']":
                    dict_input[20][i][0] = dict_input[20][i][0].replace('https://pubmed.ncbi.nlm.nih.gov/?from_uid=',"")
                    dict_input[20][i][0] = dict_input[20][i][0].replace('&linkname=assembly_pubmed',"")
                    article = dict_input[20][i][0]

            for j in range(0, (len(dict_input.columns)-3)):
                if len(dict_input[j][i]) != 0:
                    #GBADID - assertion graph
                    if str(dict_input[j][i][0]) == "genbank_assembly_accession":
                        genbank_accession = dict_input[j][i][1].replace(' (replaced)', '')
                        hash_gbad = hash_creation(genbank_accession)
                    #BIOSAMPLE - assertion graph
                    if str(dict_input[j][i][0]) == "biosample":
                        biosample = "\n    ncit:C175889 <https://www.ncbi.nlm.nih.gov/biosample" + str(dict_input[j][i][1][0]) + "> ;"
                    #BIOPROJECT - assertion graph
                    if str(dict_input[j][i][0]) == "bioproject":
                        bioproject = "\n    ncit:C175890 <https://www.ncbi.nlm.nih.gov/bioproject" + str(dict_input[j][i][1][0]) + "> ;"
                    #ISOLATE - assertion graph
                    if str(dict_input[j][i][0]) == "isolate":
                        isolate = '\n    ncit:C53471 "' + str(dict_input[j][i][1]) +'"@en ;'
                    #INFRANAME - assertion graph
                    if str(dict_input[j][i][0]) == "infraspecific_name":
                        infra_name = '\n    edam:data_1046 "' + str(dict_input[j][i][1]) + '"@en ;'
                    #GENOME_REPRESENTATION - assertion graph
                    if str(dict_input[j][i][0]) == "genome_representation":
                        gen_representation = "\n    rdf:type fbcv:" + str(dict_input[j][i][1]) + " ;"
                    #ASSEMBLY_TYPE - assertion graph
                    if str(dict_input[j][i][0]) == "assembly_type":
                        assembly_type = "\n    rdf:type " + str(dict_input[j][i][1]) + " ;"
                    #ASSEMBLY_LEVEL - assertion graph
                    if str(dict_input[j][i][0]) == "assembly_level":
                        assembly_level = "\n    ncit:C25554 " + str(dict_input[j][i][1]) + " ;"
                    #GENOME_COVERAGE - assertion graph
                    if str(dict_input[j][i][0]) == "genome_coverage":
                        genome_coverage = '\n    obi:0001939 "' + str(dict_input[j][i][1]) + '"@en ;'
                    #ASSEMBLY_METHOD - assertion graph
                    if str(dict_input[j][i][0]) == "assembly_method":
                        method = '\n    ncit:C71460 "' + str(dict_input[j][i][1]) + '"@en ;'
                    #TECH - assertion graph
                    if str(dict_input[j][i][0]) == "sequencing_technology":
                        tech = '\n    efo:0003739 "' + str(dict_input[j][i][1]) + '"@en ;'
                    #REFSEQ - assertion graph
                    if str(dict_input[j][i][0]) == "refseq_assembly_accession":
                        if len(dict_input[j][i][1]) != 3: # 3 = N/a
                            data = dict_input[j][i][1]
                            refseq_id = data.rpartition('.')[0]
                            refseq = "\n    prov:wasAssociatedWith sub:refseq ;"
                            refseq_type = ("\n\n  sub:refseq sio:SIO_000628 ncit:C45335 ;" +
                                            '\n    rdf:type "' + refseq_id +'"@en ;')
                            refseq_url_total = ("\n    edam:data_1098 <" + str(refseq_url) + "> .")
                    #WGS_PROJECT - assertion graph
                    if str(dict_input[j][i][0]) == "wgs_project":
                        wgs = '\n    prov:wasGeneratedBy sub:wgs ;'
                        wgs_project_id = "\n\n  sub:wgs sio:SIO_000628 ncit:C101294 ;" + "\n    dcterms:identifier <https://www.ncbi.nlm.nih.gov/" + str(dict_input[j][i][1][0]) + "> ;"
                    #WGS_VERSION - assertion graph
                    if str(dict_input[j][i][0]) == "wgs_project":
                        wgs_version_name = dict_input[j][i][1][0].replace("/", "")
                        wgs_version_name = wgs_version_name.replace("nuccore", "")
                        wgs_version = '\n    pav:version "' + str(wgs_version_name) + '"@en .'
                    
                    #REFSEQ_URL - assertion graph
                    if len(dict_input[21][i]) != 0:
                        if str(dict_input[21][i]) != "[' ']":
                            refseq_url = dict_input[21][i][0]

                    #SUBMITTER - prov graph
                    if str(dict_input[j][i][0]) == "submitter":
                        submitter = dict_input[j][i][1]
                    #DATE - prov graph
                    if str(dict_input[j][i][0]) == "date":
                        dict_input[j][i][1]= pd.to_datetime(dict_input[j][i][1],format='%Y-%m-%d')
                        dayprov = pd.to_datetime(dict_input[j][i][1]).day
                        monthprov = pd.to_datetime(dict_input[j][i][1]).month
                        yearprov = pd.to_datetime(dict_input[j][i][1]).year
                    #Description - prov graph
                    if len(dict_input[18][i]) != 0:            
                        if dict_input[18][i] != [' ']:
                            dict_input[18][i][0] = dict_input[18][i][0].replace('"', "'")
                            description = "\n    ncit:C101282 sub:description ;"
                            description_full = ('\n\n  sub:description a prov:Entity , dcterms:description ;' +
                                            '\n    prov:value "'+ str(dict_input[18][i][0]) +'"@en ;' +
                                            '\n    prov:wasQuotedFrom <https://www.ncbi.nlm.nih.gov/assembly/' + genbank_accession + '/> .')

                    np_prefixes = np_cnt_gbad.prefixes.format(
                        hash = hash_gbad)
                    np_head = np_cnt_gbad.head
                    np_assertions = np_cnt_gbad.assertion.format(
                    genbank_accession = genbank_accession, biosample = biosample,
                    bioproject = bioproject, infra_name = infra_name,
                    org_npub = org_npub, gen_representation = gen_representation,
                    assembly_type = assembly_type, assembly_level = assembly_level, 
                    genome_coverage = genome_coverage, refseq = refseq,
                    refseq_type = refseq_type, refseq_url_total = refseq_url_total,
                    wgs = wgs, wgs_project_id = wgs_project_id,
                    wgs_version = wgs_version, method = method, 
                    tech = tech, isolate = isolate)
                    np_prov = np_cnt_gbad.provenance.format(
                    description = description, genbank_accession = genbank_accession,
                    reference = reference, description_full = description_full,
                    submitter = submitter, dayprov = dayprov,
                    monthprov = monthprov, yearprov = yearprov, ftp = ftp)
                    np_pubinfo = np_cnt_gbad.pubinfo.format(
                    daynp = day_np, monthnp = month_np, yearnp = year_np,
                    orcid = orcid)
            
        nanopub = np_prefixes + "\n" + np_head + "\n"
        nanopub += np_assertions + "\n" + np_prov + "\n"
        nanopub += np_pubinfo
        nanopubs.append(nanopub)
        
        if search_file == True:
            convert_article_dict_to_rdf(hash_gbad, df_articles, article, orcid, np_date)    
    return nanopubs, True

# convertion of the articles to rdf trig format
def convert_article_dict_to_rdf(hash_gbad, df_articles, article, orcid, np_date):
    title = pmid = pmcid = pmcid_full = doi = ''
    doi_id = doi2 = doi_full = pub_type = abstract = keywords = ''
    authors = citing_org = org_full = journal_name = ''
    article_day = article_month = article_year = ''
    journal_url = 'https://pubmed.ncbi.nlm.nih.gov/'
    year_np = np_date[0]
    month_np = np_date[1]
    day_np = np_date[2]

    df_selected_articles = df_articles.loc[df_articles[10] == article]
    
    if len(df_selected_articles) != 0:
        df_selected_articles.reset_index(inplace=True)
        for i in range(0, len(df_selected_articles)):
            #TITLE
            if df_selected_articles[0][i] != '':
                title = df_selected_articles[0][i]
            #KEYWORDS
            if df_selected_articles[1][i] != '' and len(df_selected_articles[1][i]) != 0:
                keywords = df_selected_articles[1][i][0]
                keywords = keywords.replace("\n      \n      ",'"')
                keywords = keywords.replace("\n    ","")
                keywords = keywords.replace("; ",'"@en, "')
                keywords = "\n    prism:keyword " + keywords + '"@en ;'
            #PMID AND HASH CREATION
            if df_selected_articles[11][i] != '':
                pmid = df_selected_articles[11][i][0] 
                pmid = "https://pubmed.ncbi.nlm.nih.gov/" + pmid + "/"
                hash_art = hash_creation(pmid)
            #DOI AND PMCID
            if df_selected_articles[3][i] != '' and len(df_selected_articles[3][i][0]) != 0:
                doi_string = 'doi.org'
                pmcid_string = 'www.ncbi.nlm.nih.gov/pmc'
                if doi_string in df_selected_articles[3][i][0]:
                    doi_id = df_selected_articles[3][i][0]
                if pmcid_string in df_selected_articles[3][i][0]:
                    pmcid = " sub:paper_pmcid , "
                    pmcid_full = ("\n\n  sub:paper_pmcid a datacite:PrimaryResourceIdentifier ;" +
                    "\n    prov:value <" + str(df_selected_articles[3][i][0]) + "> ;" +
                    "\n    datacite:usesIdentifierScheme wiki:P932 .")
            if df_selected_articles[4][i] != '' and len(df_selected_articles[4][i][0]) != 0:
                doi_string = 'doi.org'
                if doi_string in df_selected_articles[4][i][0]:
                    doi2 = df_selected_articles[4][i][0]            
            if len(doi_id) == 0:
                doi_id = doi2                
            if len(doi_id) != 0:
                doi = " sub:paper_doi ,"
                doi_full = ("\n\n  sub:paper_doi a datacite:PrimaryResourceIdentifier ;" +
                "\n    prov:value <" + doi_id + "> ;" +
                "\n    datacite:usesIdentifierScheme datacite:doi ."
                )
            #PUBLICATION TYPE
            if df_selected_articles[5][i][0] != '' and df_selected_articles[5][i][0] != '\n      \n':
                pub_type = '\n    foaf:topic_interest "' + df_selected_articles[5][i][0] + '"@en ;'
            #ASSEMBLY CITATION
            if len(hash_gbad) != 0:
                citing_org = "\n    cito:extends sub:citingOrganism ;"
                org_full = ("\n\n  sub:citingOrganism a cito:citation ;" +
                "\n    cito:hasCitingEntity sub:paper_doi ;" +
                "\n    cito:hasCitationCharacterization cito:extends ;" +
                "\n    cito:hasCitingEntity <" + str(pmid) + ">;" +
                "\n    datacite:hasIdentifier sub:organism ." + "\n\n" +
                "  sub:organism a datacite:PrimaryResourceIdentifier ;" +
                "\n    prov:value <http://github.com/GenKnowlets/genknowlets/gbad/"+ str(hash_gbad) +"> ;" + 
                '\n    datacite:usesIdentifierScheme np:Nanopublication .')
            #DATE AND VOLUME
            if df_selected_articles[6][i][0] != '':
                date_volume = df_selected_articles[6][i][0]
                date = date_volume.rpartition(';')[0]
                space_count = date.count(' ')
                if space_count == 1:
                    #if "Jul-Aug" in date:
                    #    date = "2018 Jul"
                    #if "Sep-Oct 2018" in date:
                    #    date = "2018 Sep"
                    #if "Nov/Dec 2016" in date:
                    #    date 
                    if date[0].isalpha() == True:
                        newDateMonth = date[0]+date[1]+date[2]
                        newDateYear = date[-4]+date[-3]+date[-2]+date[-1]
                        date = newDateYear + " " + newDateMonth
                    date= pd.to_datetime(date,format='%Y %b')
                    article_month = pd.to_datetime(date).month
                    article_year = pd.to_datetime(date).year
                if space_count == 2:
                    date= pd.to_datetime(date,format='%Y %b %d')
                    article_day = ('\n    npdate:creationDay ' + 'npdate:' +
                    str(pd.to_datetime(date).day) + ' ;'
                    )
                    article_month = pd.to_datetime(date).month
                    article_year = pd.to_datetime(date).year
                volume_first = date_volume.rpartition(';')[2]              
                volume = volume_first.rpartition('(')[0]
                if len(volume) == 0:
                    volume = volume_first.rpartition(':')[0]
            #ABSTRACT
            if df_selected_articles[7][i] != '':
                df_selected_articles[7][i][0] = df_selected_articles[7][i][0].replace('"',"'")
                abstract = df_selected_articles[7][i][0]
            #AUTHORS
            if df_selected_articles[8][i] != '':
                authors = set(df_selected_articles[8][i])
                authors = removeref(authors)
                authors = list(authors)
                authors = ', '.join(authors)
            #JOURNAL NAME
            if df_selected_articles[9][i][0] != '':
                journal_name = df_selected_articles[9][i][0]
                if journal_name == "Acta Trop":
                    journal_url = "https://www.journals.elsevier.com/acta-tropica"
                if journal_name == "BMC Genomics":
                    journal_url = "https://bmcgenomics.biomedcentral.com/"
                if journal_name == "Genome Announc":
                    journal_url = "https://journals.asm.org/journal/mra"
                if journal_name == "PLoS Negl Trop Dis":
                    journal_url = "https://journals.plos.org/plosntds/"
                if journal_name == "Genome Biol Evol":
                    journal_url = "https://academic.oup.com/gbe"
                if journal_name == "Science":
                    journal_url = "https://www.science.org/"
                if journal_name == "Microb Genom":
                    journal_url = "https://www.microbiologyresearch.org/content/journal/mgen"

            np_prefixes = np_cnt_art.prefixes.format(hash_art = hash_art)
            np_head = np_cnt_art.head
            np_assertions = np_cnt_art.assertion.format(
            doi = doi, pmcid = pmcid, pub_type = pub_type, title = title, 
            keywords = keywords, citing_org = citing_org,
            pmid = pmid, doi_full = doi_full, pmcid_full = pmcid_full,
            abstract = abstract, org_full = org_full)
            np_prov = np_cnt_art.provenance.format(
            authors = authors, article_day = article_day, article_month = article_month,
            article_year = article_year, doi = doi, journal_name = journal_name,
            volume = volume, journal_url = journal_url, doi_id = doi_id)
            np_pubinfo = np_cnt_art.pubinfo.format(
            np_day = day_np, np_month = month_np, np_year = year_np, orcid = orcid)

            nanopub = np_prefixes + "\n" + np_head + "\n"
            nanopub += np_assertions + "\n" + np_prov + "\n"
            nanopub += np_pubinfo
            with open("../../data/output/articles.trig", "a") as f:
                f.write(nanopub)
                f.close()

def removeref(authors):
    if "\n                1\n              " in authors:
        authors.remove("\n                1\n              ")
    if "\n                2\n              " in authors:
        authors.remove("\n                2\n              ")
    if "\n                3\n              " in authors:
        authors.remove("\n                3\n              ")
    if "\n                4\n              " in authors:
        authors.remove("\n                4\n              ")
    if "\n                5\n              " in authors:
        authors.remove("\n                5\n              ")
    if "\n                6\n              " in authors:
        authors.remove("\n                6\n              ")
    if "\n                7\n              " in authors:
        authors.remove("\n                7\n              ")
    if "\n                8\n              " in authors:
        authors.remove("\n                8\n              ")
    if "\n                9\n              " in authors:
        authors.remove("\n                9\n              ")
    if "\n                10\n              " in authors:
        authors.remove("\n                10\n              ")
    if "\n                11\n              " in authors:
        authors.remove("\n                11\n              ")
    if "\n                12\n              " in authors:
        authors.remove("\n                12\n              ")
    if "\n                13\n              " in authors:
        authors.remove("\n                13\n              ")
    if "\n                14\n              " in authors:
        authors.remove("\n                14\n              ")
    if "\n                15\n              " in authors:
        authors.remove("\n                15\n              ")
    if "\n                16\n              " in authors:
        authors.remove("\n                16\n              ")
    if "\n                17\n              " in authors:
        authors.remove("\n                17\n              ")
    if "\n                18\n              " in authors:
        authors.remove("\n                18\n              ")
    if "\n                19\n              " in authors:
        authors.remove("\n                19\n              ")
    if "\n                20\n              " in authors:
        authors.remove("\n                20\n              ")
    if "\n                21\n              " in authors:
        authors.remove("\n                21\n              ")
    if "\n                22\n              " in authors:
        authors.remove("\n                22\n              ")
    if "\n                23\n              " in authors:
        authors.remove("\n                23\n              ")

    return authors

def convert_rdf_to_file(nanopubs, filepath):
    writemode = "a"
    output_folder = "../../data/output"

    for i in range(len(nanopubs)):
        filename = filepath.replace("\\", "/").split("/")[-1]
        filename_without_extension = filename.split(".")[0]
        output_path = f"{output_folder}/{filename_without_extension}.trig"
        with open(output_path, writemode) as f:
            f.write(nanopubs[i])
            f.close()

if __name__ == "__main__":

    np_date = date()
    orcid = orcid()
    print('Starting converting organism data to nanopublication.')
    filepath_org = "../../data/staging_data/org/organism.json"
    file_as_dict = extract_dict_from_file(filepath_org)
    hash_org = hash_creation(file_as_dict[0]["tax_id"])
    nanopubs = convert_org_dict_to_rdf(file_as_dict, hash_org, orcid, np_date)
    convert_rdf_to_file(nanopubs[0], filepath_org)
    if nanopubs[1] == True:
        print('Organism nanopub generation - Done')

    print('Starting converting GBAD and article data to nanopublication.')
    filepath_gbad = "../../data/staging_data/gbad/formatted_gbad_data.json"
    file_as_dict = extract_dict_from_file(filepath_gbad)
    df_gbad = pd.read_json(filepath_gbad)
    df = pd.DataFrame(df_gbad.values.tolist())
    nanopubs = convert_gbad_dict_to_rdf(df, hash_org, orcid, np_date)
    filepath_gbad_final = "../../data/staging_data/gbad/gbad.json"
    convert_rdf_to_file(nanopubs[0], filepath_gbad_final)