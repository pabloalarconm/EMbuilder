from embuilder.builder import EMB

prefixes = dict(
  rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#" ,
  rdfs = "http://www.w3.org/2000/01/rdf-schema#" ,
  obo = "http://purl.obolibrary.org/obo/" ,
  sio = "http://semanticscience.org/resource/" ,
  this = "http://marks.test/this/" ,
  dc = "http://purl.org/dc/elements/1.1/")

triplets = [["http://www.subject.org/","http://www.predicate.org/","http://www.object.org/", "iri"],
                ["http://www.subject1.org/","http://www.predicate2.org/","http://www.object3.org/", "iri"]]

config = dict(
  source_name = "source_cde_test"
)

yarrrml = EMB(config)
test = yarrrml.transform(prefixes, triplets)
print(test)