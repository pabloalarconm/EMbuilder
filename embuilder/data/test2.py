prefixes = {
  "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#" ,
  "sio" : "http://semanticscience.org/resource/" ,
  "this" : "http://my_example.com/"
  }
triplets = [
  ["this:$(pid)_$(uniqid)_ID","sio:SIO_000020","this:$(pid)_$(uniqid)_Birthdate_Role","iri"],
  ["this:$(pid)_$(uniqid)_ID","sio:SIO_000300","$(sexLabel)","xsd:string"]]

config = {
  "source_name" : "source_cde_test",
  "configuration" : "ejp",                
  "csv_name" : "source_1"
}

