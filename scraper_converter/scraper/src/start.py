import sys
import os
import wget
import pandas as pd
from sty import bg
import datetime
pd.options.mode.chained_assignment = None

# FILE DESCRIPTION
# This is the first script to be executed to run the 
# scraper and converter of GenBank instances.
#
# The script can be processed as follow:
# python start.py option
# Options:
#   preloaded : Uses the url.txt as the starter file to process all the urls presented in the same file
#   ncbi : Donwload the file contain all the data and metadata present in GenBank.
#          Extract all the information in one run!!
           ##
           ##Need to implement that!
           ##
#   name : Uses the same dowloaded GenBank file. Although, search by the GENO name of the organism.
#          Example: Right -> Trypanosoma
#                   Wrong -> Trypanosoma Cruzi
           ##
           ##Need to implement that!
           ##
#   <url> : Only extract the organism provided by the given url.

# Calculating the execution time
begin_time = datetime.datetime.now()

#Using the preloaded urls.txt
if sys.argv[1] == "preloaded":
    with open('../../data/staging_data/urls.txt') as f:
        lines = f.readlines()
    for i in range (0, len(lines)):
        assembly_url=lines[i]
        cmdStart = "python main.py " + str(assembly_url)
        os.system(cmdStart)

# Using the full eukaryotes.txt file
if sys.argv[1] == "ncbi":
    #df = pd.read_csv('eukaryotes.txt', delimiter = "\t")
    df = pd.read_csv('../../data/supporting_files/eukaryotes_part.txt', delimiter = "\t")
   
   # Dropping TAXID duplicates and organism name duplicates
    df = df.drop_duplicates(subset='TaxID', keep='first')
    new = df['#Organism/Name'].str.split(' ', n = 2, expand = True)
    df["repeat"]= new[1]
    df.drop_duplicates(subset ='repeat',keep = 'first', inplace = True)

    df['Assembly Accession'] = 'https://www.ncbi.nlm.nih.gov/assembly/' + df['Assembly Accession'].astype(str)
    for i in range (0, len(df)):
        # reseting the index
        right_org = right_org.reset_index(drop=True)
        message = bg.da_red + 'Starting the scrape and convertion of ' + str(df['#Organism/Name'][i]) + ' organism to nanopubs. =)'+ bg.rs
        print(message)
        assembly_url=df['Assembly Accession'][i]
        cmdStart = "python main.py " + str(assembly_url)
        os.system(cmdStart)

# Searching by a name in the eukaryotes.txt file
if sys.argv[1] == 'name':
    org_name = input('Enter the genus organism name: ')
    org_name = org_name.replace(' ', '')
    org_name = org_name.lower() + ' '
    
    search_file = os.path.isfile('eukaryotes.txt')
    if search_file == False:
        link = 'https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/eukaryotes.txt'
        wget.download(link)
    
    file = pd.read_csv('eukaryotes.txt', delimiter = "\t")
    file.sort_values('#Organism/Name', inplace = True)
    file['#Organism/Name'] = file['#Organism/Name'].str.lower()
    
    # removing duplicates
    right_org = file.loc[file['#Organism/Name'].str.contains(org_name, case=False)]
    right_org.drop_duplicates(subset ='TaxID',keep = 'first', inplace = True)

    # removing duplicates second sub string
    new = right_org['#Organism/Name'].str.split(' ', n = 2, expand = True)
    right_org["genus"]= new[0]
    right_org["repeat"]= new[1]
    right_org.drop_duplicates(subset ='repeat',keep = 'first', inplace = True)
    org_name = org_name.replace(' ', '')
    right_org = right_org[right_org['genus'] == org_name]    
    print(right_org)
    print(' ')
    answer = input(str(len(right_org.index)) + ' different organisms were found. Extract all of them? (Y: yes / N: no) ')
    
    if answer == 'Y' or answer == 'y':
        # reseting the index
        right_org = right_org.reset_index(drop=True)
        # adding url prefix to start scraping and conversion
        right_org['Assembly Accession'] = 'https://www.ncbi.nlm.nih.gov/assembly/' + right_org['Assembly Accession'].astype(str)
        for i in range(0, len(right_org)):
            message = bg.da_red + 'Starting the scrape and convertion of ' + str(right_org['#Organism/Name'][i]) + ' organism to nanopubs. =)'+ bg.rs
            print(message)
            cmdStart = "python main.py " + right_org['Assembly Accession'][i]
            os.system(cmdStart)
    if answer == 'N' or answer == 'n':
        cmdStart = "python start.py name"
        os.system(cmdStart)
    else:
       print('End!')

# A faster way to extract by name using a .txt file (same flow of name)
if sys.argv[1] == 'nametxt':
    with open("../../data/supporting_files/100_organism.txt") as f:
        lines = f.readlines()
    for i in range (0, len(lines)):
        org_name = lines[i]
        org_name = org_name.replace("\n","")
        org_name = org_name.replace(' ', '')
        org_name = org_name.lower() + ' '
        
    
        search_file = os.path.isfile('eukaryotes.txt')
        if search_file == False:
            link = 'https://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/eukaryotes.txt'
            wget.download(link)
    
        file = pd.read_csv('eukaryotes.txt', delimiter = "\t")
        file.sort_values('#Organism/Name', inplace = True)
        file['#Organism/Name'] = file['#Organism/Name'].str.lower()

        # removing duplicates
        right_org = file.loc[file['#Organism/Name'].str.contains(org_name, case=False)]
        right_org.drop_duplicates(subset ='TaxID',keep = 'first', inplace = True)
        
        # check if org_name is in the GenBank database.\
        if not right_org.empty:   

            # removing duplicates second sub string
            new = right_org['#Organism/Name'].str.split(' ', n = 2, expand = True)
            right_org["genus"]= new[0]
            right_org["repeat"]= new[1]
            right_org.drop_duplicates(subset ='repeat',keep = 'first', inplace = True)
            org_name = org_name.replace(' ', '')
            right_org = right_org[right_org['genus'] == org_name]

            # reseting the index
            right_org = right_org.reset_index(drop=True)
            print(right_org)
            # adding url prefix to start scraping and conversion
            right_org['Assembly Accession'] = 'https://www.ncbi.nlm.nih.gov/assembly/' + right_org['Assembly Accession'].astype(str)
            for i in range(0, len(right_org)):
                message = bg.da_red + 'Starting the scrape and convertion of ' + str(right_org['#Organism/Name'][i]) + ' organism to nanopubs. =)'+ bg.rs
                print(message)
                cmdStart = "python main.py " + right_org['Assembly Accession'][i]
                os.system(cmdStart)
        

# Normal one (same as python main.py <url>)
else:
    assembly_url=sys.argv[1]
    if ('http' not in assembly_url) or (len(assembly_url) == 0):
        print("Wrong input")
        exit
    else:
        cmdStart = "python main.py " + str(assembly_url)
        os.system(cmdStart)

total_time = str(datetime.datetime.now() - begin_time)
file_summary = open("../../data/total_time.txt","a+")
file_summary.write(total_time)
file_summary.close()