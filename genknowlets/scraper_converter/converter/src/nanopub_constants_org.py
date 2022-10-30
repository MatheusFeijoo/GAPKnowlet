prefixes = """
@prefix this: <http://github.com/GenKnowlets/genknowlets/org/{hash}> .
@prefix sub: <http://github.com/GenKnowlets/genknowlets/org/{hash}#> .
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
@prefix ncbi_taxID: <https://www.ncbi.nlm.nih.gov/taxonomy/browser/wwwtax.cgi?id> .
@prefix xsd: <http://www.w3.org/tr/xmlschema11-2/#> .
@prefix eco: <https://evidenceontology.org/term/> .
"""

head = """sub:Head {
  this: np:hasAssertion sub:assertion ;
    np:hasProvenance sub:provenance ;
    np:hasPublicationInfo sub:pubinfo ;
    a np:Nanopublication .
}
"""

assertion = """sub:assertion {{
  ncbi_taxID:{tax_id} sio:SIO_000628 sio:SIO_010000 ;
    foaf:name "{organism_name}"@en ;
    rdf:type ncit:C25796 ;
    ncit:C101282 edam:data_0925 ;
    ncit:C67045 <https://www.ncbi.nlm.nih.gov/{representative_genome}> .

  edam:data_0925 ncit:C25256 "{qnt_assemblies}"^^xsd:integer .
}}
"""

provenance = """sub:provenance {{
  sub:assertion a prov:Entity ;
    prov:wasGeneratedBy sub:automaticAssertion ;
    pav:authoredBy sub:author ;{description}
    ncit:C101282 sub:citation ;
    prov:hadPrimarySource <{url_tax}> , <https://www.ncbi.nlm.nih.gov/genome/?term=txid{tax_id}> ;
    dcterms:accessRights <https://www.ncbi.nlm.nih.gov/home/about/policies/> .

  sub:author a prov:Agent , foaf:organization , ncit:C45799 ;
    foaf:name "NCBI - National Center for Biotechnology Information"@en ;
    dcterms:source <https://www.ncbi.nlm.nih.gov/> . 

  sub:automaticAssertion a prov:Activity , eco:0000203;
    prov:wasAssociatedWith sub:author ;
    dcterms:dateSubmitted "DATETIME"^^xsd:datetime ;
    ncit:C25301 npdate:{prov_day} ;
    ncit:C29846 npdate:{prov_month} ;
    ncit:C29848 npdate:{prov_year} . {description_total}

  sub:citation a prov:Entity , dcterms:bibliographicCitation ;
    dcterms:source <https://doi.org/10.1093/database/baaa062> ;
    prov:value "Schoch CL, et al. NCBI Taxonomy: a comprehensive update on curation, resources and tools. Database (Oxford). 2020: baaa062."@en . 
}}
"""

pubinfo = """sub:pubinfo {{
  this: a prov:Entity ;
    pav:authoredBy sub:author ;
    prov:wasDerivedFrom sub:dataSource ;
    pav:createdWith sub:software ;
    prov:wasGeneratedBy sub:automaticAssertion ;   
    prov:hadPrimarySource <{url_tax}> , <https://www.ncbi.nlm.nih.gov/genome/?term=txid{tax_id}> ;
    dcterms:accessRights <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:subject sio:SIO_010000 .
  
  sub:author a prov:Agent ;
    dcterms:cretor {orcid} .

  sub:dataSource a prov:Agent , foaf:organization , ncit:C45799 ;
    foaf:name "NCBI - National Center for Biotechnology Information"@en ;
    dcterms:source <https://www.ncbi.nlm.nih.gov/> . 

  sub:software a prov:Agent , prov:softwareAgent ;
    foaf:name "GAPscraper"@en ;
    pav:version "1.0"^^xsd:integer ;
    pav:authoredBy <https://orcid.org/0000-0001-9582-4595> , <https://orcid.org/0000-0002-0943-5356> , <https://orcid.org/0000-0002-0792-8157> , <https://orcid.org/0000-0002-7930-612X> ;
    edam:data_1188 <https://doi.org/10.5281/zenodo.4818638> ;
    dcterms:source <https://github.com/MatheusFeijoo/Genome-Assembly-nanoPublication> .
    
  sub:automaticAssertion a prov:Activity , eco:0000203 ;
    prov:wasAssociatedWith sub:author , sub:dataSource , sub:software ;
    dcterms:dateSubmitted "DATETIME"^^xsd:datetime ;
    ncit:C25301 npdate:{np_day} ;
    ncit:C29846 npdate:{np_month} ;
    ncit:C29848 npdate:{np_year} .
}}
"""