prefixes = """
@prefix this: <http://github.com/GenKnowlets/genknowlets/art/{hash_art}> .
@prefix sub: <http://github.com/GenKnowlets/genknowlets/art/{hash_art}#> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix pav: <http://purl.org/pav/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix sio: <http://semanticscience.org/resource/> .
@prefix foaf: <http://xmlns.com/foaf/spec/#term_> .
@prefix ncit: <http://ncithesaurus.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=> .
@prefix edam: <http://edamontology.org/> .
@prefix npdate: <http://github.com/GenKnowlets/npdate/> .
@prefix xsd: <http://www.w3.org/tr/xmlschema11-2/#> .
@prefix eco: <https://evidenceontology.org/term/> .
@prefix so: <http://purl.obolibrary.org/obo/SO_> .
@prefix datacite: <http://purl.org/spar/datacite> .
@prefix prism: <http://prismstandard.org/namespaces/basic/2.0/> .
@prefix doi: <http://dx.doi.org/> .
@prefix wiki: <http://www.wikidata.org/wiki/Property:> .
@prefix cito: <http://purl.org/spar/cito> .
@prefix fabio: <http://purl.org/spar/fabio> .
@prefix pmid: <http://pubmed.ncbi.nlm.nih.gov/> .
@prefix dbpedia: <https://dbpedia.org/resource> .
"""

head = """sub:Head {
  this: np:hasAssertion sub:assertion ;
    np:hasProvenance sub:provenance ;
    np:hasPublicationInfo sub:pubinfo ;
    a np:Nanopublication .
}
"""

assertion = """sub:assertion {{
  this: a fabio:journalArticle ;
    datacite:hasIdentifier{doi}{pmcid} sub:paper_pmid ;{pub_type}
    dcterms:language dbpedia:English_language ;
    dcterms:title "{title}"@en ;{keywords}{citing_org}
    datacite:hasDescription sub:abstract .

  sub:paper_pmid a datacite:PrimaryResourceIdentifier ;
    prov:value <{pmid}> ;
    datacite:usesIdentifierScheme edam:data_1187 .{doi_full}{pmcid_full}

  sub:abstract datacite:hasDescriptionType datacite:abstract ;
    prov:value "{abstract}"@en .{org_full}
}}
"""

provenance = """sub:provenance {{
  sub:assertion a prov:Entity ;
    prov:wasGeneratedBy sub:journalPublication ;
    pav:authoredBy sub:authors ;
    prov:wasDerivedFrom sub:journal ;
    prov:hadPrimarySource sub:paper_doi ;
    dcterms:accessRights <https://www.ncbi.nlm.nih.gov/home/about/policies/> .

  sub:authors a prov:Agent ;
    foaf:name "{authors}"@en .

  sub:journal a prov:Agent , fabio:Journal ;
    foaf:name "{journal_name}"@en ;
    prism:volume "{volume}"^^xsd:integer ;
    dcterms:source <{journal_url}> .

  sub:journalPublication a prov:Activity , eco:0006016 ;
    prov:wasAssociatedWith sub:authors , sub:journal ;
    dcterms:dateSubmitted "DATETIME"^^xsd:datetime;{article_day}
    npdate:creationMonth npdate:{article_month} ;
    npdate:creationYear npdate:{article_year} .

  sub:paper_doi a prov:Entity , datacite:PrimaryResourceIdentifier ;
    prov:value <{doi_id}> ;
    datacite:usesIdentifierScheme datacite:doi .  
    

}}
"""

pubinfo = """sub:pubinfo {{
  this: a prov:Entity ;
    pav:authoredBy sub:authors ;
    prov:wasDerivedFrom sub:dataSource ;
    pav:createdWith sub:software ;
    prov:wasGeneratedBy sub:automaticAssertion ;
    prov:hadPrimarySource <https:///pubmed.ncbi.nlm.nih.gov/> ;
    dcterms:accessRights <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:subject so:0001248 , sio:SIO_010055 , fabio:journalArticle .

  sub:authors a prov:Agent;
    dcterms:creator {orcid} .
  
  sub:dataSOurce a prov:Agent , foaf:organization , ncit:C42881 ;
    foaf:name "PubMed"@en ;
    dcterms:source <http://pubmed.ncbi.nlm.nih.gov/> . 

  sub:software a prov:Agent , prov:softwareAgent ; 
    foaf:name "GAPscraper"@en ;
    pav:version "1.0"^^xsd:integer ;
    pav:authoredBy <https://orcid.org/0000-0001-9582-4595> , <https://orcid.org/0000-0002-0943-5356> , <https://orcid.org/0000-0002-0792-8157> , <https://orcid.org/0000-0002-7930-612X> ;
    edam:data_1188 <https://doi.org/10.5281/zenodo.4818638> ;
    dcterms:source <https://github.com/MatheusFeijoo/Genome-Assembly-nanoPublication> .
    
  sub:automaticAssertion a prov:Activity , eco:0000203 ;
    prov:wasAssociatedWith sub:authors , sub:dataSource , sub:software ;
    dcterms:dateSubmitted "DATETIME"^^xsd:datetime ;
    npdate:creationDay npdate:{np_day} ;
    npdate:creationMonth npdate:{np_month} ;
    npdate:creationYear npdate:{np_year} .
}}
"""