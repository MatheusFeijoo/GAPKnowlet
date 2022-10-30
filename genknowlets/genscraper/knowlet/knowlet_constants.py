prefixes = """
@prefix this: <http://github.com/GenKnowlets/genknowlets/knowlet/{hash}> .
@prefix sub: <http://github.com/GenKnowlets/genknowlets/knowlet/{hash}#> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix pav: <http://purl.org/pav/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-sytanx-ns#> .
@prefix foaf: <http://xmlns.com/foaf/spec/#term_> .
@prefix ncit: <http://ncithesaurus.nci.nih.gov/ncitbrowser/ConceptReport.jsp?dictionary=NCI_Thesaurus&ns=ncit&code=> .
@prefix xsd: <http://www.w3.org/tr/xmlschema11-2/#> .
@prefix eco: <https://evidenceontology.org/term/> .
@prefix edam: <http://edamontology.org/> .
@prefix datacite: <http://purl.org/spar/datacite> .
@prefix ro: <http://purl.obolibrary.org/obo/RO_> .
@prefix obi: <http://purl.obolibrary.org/obo/OBI_> .
@prefix npdate: <http://github.com/GenKnowlets/npdate/> .
"""

head = """sub:Head {
  this: np:hasAssertion sub:assertion ;
    np:hasProvenance sub:provenance ;
    np:hasPublicationInfo sub:pubinfo ;
    a np:Nanopublication .
    a "knowlet"@en .
}
"""

assertion = """sub:assertion {{
  this: a ncit:C47846 ;
    prov:wasDerivedFrom sub:CardinalAssertion ;{other_knowlet} 
    dcterms:subject "{subject}"@en .
  
  sub:CardinalAssertion a prov:collection ;
 {nanopubs}{other_knowlet_full}
}}
"""

provenance = """sub:provenance {{
  sub:assertion a prov:Entity ;
    prov:wasGeneratedBy sub:knowletActivity ;
    pav:authoredBy sub:author ;
    pav:hasCurrentVersion "{current_version}"@en ;{revision}
    dcterms:accessRights <https://creativecommons.org/licenses/by/4.0/> .

  sub:authors a prov:Agent ;
    dcterms:creator <https://orcid.org/0000-0001-9582-4595> , <https://orcid.org/0000-0002-0943-5356> , <https://orcid.org/0000-0002-0792-8157> , <https://orcid.org/0000-0002-7930-612X> ; ;
    prov:actedOnBehalfOf sub:organization .

  sub:organization a prov:Agent, prov:Organization ;
    foaf:name "Universidade Federal do Rio de Janeiro"@en , "Fundação Oswaldo Cruz"@en .

  sub:knowletActivity a prov:Activity , ncit:C47846 ; 
    prov:wasAssociatedWith sub:author ;
    dcterms:dateSubmitted "DATETIME"^^xsd:datetime ;
    ncit:C25301 npdate:{dayprov} ;
    ncit:C29846 npdate:{monthprov} ;
    ncit:C29848 npdate:{yearprov} .

}}
"""

pubinfo = """sub:pubinfo {{
  this: a prov:Entity ;
    pav:authoredBy sub:authors ;
    pav:createdWith sub:software
    prov:wasGeneratedBy sub:manualAssertion ;
    dcterms:accessRights <https://creativecommons.org/licenses/by/4.0/> ;
    prism:keywords {keywords}"@en, "knowlet"@en , ncit:C47846.

  sub:author a prov:Agent ;
    dcterms:creator <https://orcid.org/0000-0001-9582-4595> , <https://orcid.org/0000-0002-0943-5356> , <https://orcid.org/0000-0002-0792-8157> , <https://orcid.org/0000-0002-7930-612X> ; .

  sub:software a prov:Agent , prov:softwareAgent ; 
    foaf:name "KnowletGenerator"@en ;
    pav:version "1.0"^^xsd:integer ;
    pav:authoredBy <https://orcid.org/0000-0001-9582-4595> , <https://orcid.org/0000-0002-0943-5356> , <https://orcid.org/0000-0002-0792-8157> , <https://orcid.org/0000-0002-7930-612X> ;
    edam:data_1188 <https://doi.org/10.5281/zenodo.4818638> ;
    dcterms:source <https://github.com/MatheusFeijoo/Genome-Assembly-nanoPublication> .

  sub:manualAssertion a prov:Activity , eco:0000218 ;
    prov:wasAssociatedWith sub:author, sub:software ;
    dcterms:dateSubmitted "DATETIME"^^xsd:datetime ;
    ncit:C25301 npdate:{daynp} ;
    ncit:C29846 npdate:{monthnp} ;
    ncit:C29848 npdate:{yearnp} .
}}
"""