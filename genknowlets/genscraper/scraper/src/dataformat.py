from items import AssembliesItems
import pandas as pd
import re as re
import shutil


# newdf = 'https://pubmed.ncbi.nlm.nih.gov/?from_uid=' + bn[20].astype(str) + '&linkname=assembly_pubmed'
# newdf = newdf.replace("'","")
#print(bn[20])
# newdf.to_csv('teste.txt', header=False, index=False)


df = pd.read_json('../../data/staging_data/assemblies.json')
#print (df)
bn = pd.DataFrame(df.values.tolist())


#print(bn[x][y][z])
#x = Column -> GBAD instances
#y = Line -> GBAD instances
#z = Inside the colum (0),(1)

for i in range(0, (len(bn.columns)-3)): # -3 -> 3 last columns not follow [][][]
    for j in range(0, len(bn)):
        if bn[i][j] != []:
            if bn[i][j][0] == "Infraspecific name: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "Isolate: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "") 
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "Sex: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "") 
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "Submitter: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "") 
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].lower()
        
            if bn[i][j][0] == "Date: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")  
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].lower()
        
            if bn[i][j][0] == "Assembly level: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()
                if bn[i][j][1] == "Chromosome":
                    bn[i][j][1] = "ncit:C13202"
                else:
                    if bn[i][j][1] == "Complete Genome":
                        bn[i][j][1] = "ncit:C16629"
                    else:
                        if bn[i][j][1] == "Scaffold":
                            bn[i][j][1] = "gfvo:Scaffold"
                        else:
                            if bn[i][j][1] == "Contig":
                                bn[i][j][1] = "gfvo:Contig"

            if bn[i][j][0] == "Assembly type: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()
                if bn[i][j][1] == "haploid":
                    bn[i][j][1] = "pato:0001375"
                else:
                    if bn[i][j][1] == "haploid-with-alt-loci":
                        bn[i][j][1] = "mesh:D056426"
                    else:
                        if bn[i][j][1] == "alternate-pseudohaplotype":
                            bn[i][j][1] = "'pseudohaplotype assemblies'@en"
                        else:
                            if bn[i][j][1] == "diploid":
                                bn[i][j][1] = "pato:0001394"
                            else:
                                if bn[i][j][1] == "unresolved-diploid":
                                    bn[i][j][1] = "'unresolved diploid'@en"
                                else:
                                    if bn[i][j][1] == "assembly":
                                        bn[i][j][1] = "so:0001248"

            if bn[i][j][0] == "Genome representation: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()
                if bn[i][j][1] == "full":
                    bn[i][j][1] = "0003237"
                else:
                    if bn[i][j][1] == "partial":
                        bn[i][j][1] = "0003238"

            if bn[i][j][0] == "RefSeq category: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "GenBank assembly accession: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")
                bn[i][j][1] = bn[i][j][1].replace(" (latest)","")
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "RefSeq assembly accession: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()


            if bn[i][j][0] == "RefSeq assembly and GenBank assembly identical: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "Synonyms: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")    
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "Expected final version: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")    
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "Genome coverage: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")    
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "Sequencing technology: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "") 
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "Assembly method: ":
                bn[i][j][1] = bn[i][j][1].replace("<dd>", "")
                bn[i][j][1] = bn[i][j][1].replace("</dd>", "")     
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()
        
            if bn[i][j][0] == "BioSample: ":
                bn[i][j][1] = re.findall(r'"([^"]*)"', bn[i][j][1])
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "BioProject: ":
                bn[i][j][1] = re.findall(r'"([^"]*)"', bn[i][j][1])
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].lower()

            if bn[i][j][0] == "WGS Project: ":
                bn[i][j][1] = re.findall(r'"([^"]*)"', bn[i][j][1])
                bn[i][j][0] = bn[i][j][0].replace(": ", "")
                bn[i][j][0] = bn[i][j][0].replace(" ", "_")
                bn[i][j][0] = bn[i][j][0].lower()

    index = bn.index
    
        #bn[20][i][0] = bn[20][i][0].replace(" [UID] ", "")
        #bn[20][i][0] = 'https://pubmed.ncbi.nlm.nih.gov/?from_uid=' + bn[20][i][0] + '&linkname=assembly_pubmed'

for i in range(0, (len(bn))):
    if len(bn[18][i]) != 0:          
        if len(bn[18][i][0]) == 1:
            bn[18][i][0] = ""
        bn[18][i][0] = bn[18][i][0].replace('\n','')
        #bn[20] = df[20].drop(labels=i, axis=0)

updated_assemblies = []

articles = open("../../data/staging_data/articles_links.txt", "a")
for i in range(0, len(bn)):
        if len(bn[20][i]) != 0:
            bn[20][i][0] = bn[20][i][0].replace(" [UID] ", "")
            bn[20][i][0] = 'https://pubmed.ncbi.nlm.nih.gov/?from_uid=' + bn[20][i][0] + '&linkname=assembly_pubmed'
            articles.write(bn[20][i][0] + "\n")
        # else:
        #     try:
        #         updated_assemblies.append(bn[21][i][0])
        #     except:
        #         print("Error during articles links collection")
        #         path = shutil.copyfile("../../data/supporting_files/articles_links.txt","../../data/staging_data/articles_linksFAIL.txt")
        

data = df.to_json(r'../../data/staging_data/gbad/formatted_gbad_data.json', orient="records")
print(data)

## Assemblies that have been updated and the ncbi .txt file is not updated yet
assemblies_nscrapped = open("../../data/supporting_files/assemblies_notscrapped.txt", "a")
for i in range(0, len(updated_assemblies)):
    assemblies_nscrapped.write(updated_assemblies[i] + "\n")