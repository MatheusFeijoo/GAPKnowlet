prefixes = """
@prefix this: <http://github.com/GenKnowlets/genknowlets/gbad/{hash}> .
@prefix sub: <http://github.com/GenKnowlets/genknowlets/{hash}#> .
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
@prefix ncbi_asbID: <https://www.ncbi.nlm.nih.gov/assembly/> .
@prefix fbcv: <http://purl.obolibrary.org/obo/FBcv_> .
@prefix pato: <http://purl.obolibrary.org/obo/PAto> .
@prefix so: <http://www.sequenceontology.org/browser/current_release/term/SO:> .
@prefix ero: <https://purl.obolibrary.org/obo/ERO_> .
@prefix obi: <https://purl.obolibrary.org/obo/OBI_> .
@prefix efo:  <http://www.ebi.ac.uk/efo/> .
@prefix mesh: <http://purl.bioontology.org/ontology/MESH/> .
@prefix gfvo: <https://www.codamono.com/biointerchange/gfvo#> .
"""

head = """sub:Head {
  this: np:hasAssertion sub:assertion ;
    np:hasProvenance sub:provenance ;
    np:hasPublicationInfo sub:pubinfo ;
    a np:Nanopublication .
}
"""

assertion = """sub:assertion {{
  this: a edam:data_2292 , edam:data_0925 ;
    prov:wasGeneratedBy sub:gbAssembly ;{refseq}{wgs}{biosample}{bioproject}
    sio:SIO_000628 sub:strain .

  sub:strain sio:SIO_000628 sio:SIO_010055 ;{infra_name}{isolate}
    sio:SIO_000497 <http://github.com/GenKnowlets/genknowlets/org/{org_npub}> .

  <http://github.com/GenKnowlets/genknowlets/org/{org_npub}> sio:SIO_000628 sio:SIO_010000 .

  sub:gbAssembly sio:SIO_000628 so:SO_0001248 ;{gen_representation}{assembly_type}{assembly_level}{method}{tech}{genome_coverage}{refseq}    
    rdf:type ncit:C164815 .{refseq_type}{refseq_url_total}{wgs_project_id}{wgs_version}
}}
"""

provenance = """sub:provenance {{
  sub:assertion a prov:Entity ; 
    prov:wasGeneratedBy sub:automaticAssertion ; 
    pav:authoredBy sub:submitter ; 
    pav:curatedBy sub:repository ;{description} 
    prov:wasDerivedFrom sub:ftp ;
    prov:hadPrimarySource <https://www.ncbi.nlm.nih.gov/assembly/{genbank_accession}> ;
    dcterms:accessRights <https://www.ncbi.nlm.nih.gov/home/about/policies/> .
    
  sub:submitter a prov:Agent , foaf:organization ;
    foaf:name "{submitter}"@en .

  sub:repository a prov:Agent , foaf:organization , ncit:C45799 ;
    foaf:name "NCBI - National Center for Biotechnology Information"@en ;
    dcterms:source <https://www.ncbi.nlm.nih.gov/> .

  sub:automaticAssertion a prov:Activity , eco:0000203;
    prov:wasAssociatedWith sub:repository , sub:repository ;
    dcterms:dateSubmitted "DATETIME"^^xsd:datetime ;
    npdate:creationDay npdate:{dayprov} ;
    npdate:creationMonth npdate:{monthprov} ;
    npdate:creationYear npdate:{yearprov} .{description_full}

  sub:ftp a prov:Entity , dcterms:dataset ;
    prov:hadPrimarySource <{ftp}>.
}}
"""

pubinfo = """sub:pubinfo {{
  this: a prov:Entity ;
    pav:authoredBy sub:authors ;
    prov:wasDerivedFrom sub:dataSource ;
    pav:createdWith sub:software ;
    prov:wasGeneratedBy sub:automaticAssertion ;
    prov:hadPrimarySource <https://www.ncbi.nlm.nih.gov/assembly/> ;
    dcterms:accessRights <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:subject so:0001248 , sio:SIO_010055 .

  sub:authors a prov:Agent;
    dcterms:creator {orcid}.

  sub:dataSource a prov:Agent , foaf:organization , ncit:C45799 ;
    foaf:name "NCBI - National Center for Biotechnology Information"@en .
    dcterms:source <https://www.ncbi.nlm.nih.gov/> .    

  sub:software a prov:Agent , prov:softwareAgent ;
    foaf:name "GAPscraper"@en ;
    pav:version "1.0"^^xsd:integer ;
    pav:authoredBy <https://orcid.org/0000-0001-9582-4595> , <https://orcid.org/0000-0002-0943-5356> , <https://orcid.org/0000-0002-0792-8157> , <https://orcid.org/0000-0002-7930-612X> ;
    edam:data_1188 <https://doi.org/10.5281/zenodo.4818638> ;
    dcterms:source <https://github.com/MatheusFeijoo/Genome-Assembly-nanoPublication> .

  sub:automaticAssertion a prov:Activity , eco:0000203 ;
    prov:wasAssociatedWith sub:authors , sub:dataSource , sub:software ;
    dcterms:dateSubmitted "DATETIME"^^xsd:datetime ;
    npdate:creationDay npdate:{daynp} ;
    npdate:creationMonth npdate:{monthnp} ;
    npdate:creationYear npdate:{yearnp} .
}}
"""