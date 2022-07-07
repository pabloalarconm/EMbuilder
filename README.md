# **EMbuilder** 
## **Etemenanki Builder**

**Template builder for multiple Linked Data representations:**
* **[YARRRML](https://rml.io/yarrrml/spec/)**
* **OBDA** (Ontology Based Database Acccess)
* **[ShEx (Shape Expression)](http://shex.io/shex-semantics/index.html)**
* **[SPARQL 1.1 ](https://www.w3.org/TR/sparql11-overview/)**


### **Instalation:** 
```
pip install EMbuilder
```
### **Use case:** 
It consumes JSON object with all **prefixes**, **triplets** (including object's **datatype**) and **configuration** parameter as data input. You can use this example (below) or you can use [test.py](https://github.com/pabloalarconm/EMbuilder/blob/main/test/test.py) as an use case for creating your templates based on one of [EJP-RD Common Data Elements](https://github.com/ejp-rd-vp/CDE-semantic-model):

```python
from embuilder.builder import EMB

data = {
  "prefixes" : {
    "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#" ,
    "rdfs" : "http://www.w3.org/2000/01/rdf-schema#" ,
    "obo" : "http://purl.obolibrary.org/obo/" ,
    "sio" : "http://semanticscience.org/resource/" ,
    "xsd" : "http://www.w3.org/2001/XMLSchema#",
    "this" : "http://my_example.com/"},

  "triplets" : [
    ["this:$(pid)_$(uniqid)_ID","sio:denotes","this:$(pid)_$(uniqid)_Role","iri"],
    ["this:$(pid)_$(uniqid)_Entity","sio:has-role","this:$(pid)_$(uniqid)_Role","iri"],
    ["this:$(pid)_$(uniqid)_Role","sio:is-realized-in","this:$(pid)_$(uniqid)_Process","iri"],
    ["this:$(pid)_$(uniqid)_Process","sio:has-output","this:$(pid)_$(uniqid)_Output","iri"],
    ["this:$(pid)_$(uniqid)_Output","sio:refers-to","this:$(pid)_$(uniqid)_Attribute","iri"],
    ["this:$(pid)_$(uniqid)_Entity","sio:has-attribute","this:$(pid)_$(uniqid)_Attribute","iri"],

    ["this:$(pid)_$(uniqid)_ID","rdf:type","sio:identifier","iri"],
    ["this:$(pid)_$(uniqid)_Entity","rdf:type","sio:person","iri"],
    ["this:$(pid)_$(uniqid)_Role","rdf:type","sio:role","iri"],
    ["this:$(pid)_$(uniqid)_Process","rdf:type","sio:process","iri"],
    ["this:$(pid)_$(uniqid)_Output","rdf:type","sio:information-content-entity","iri"],
    ["this:$(pid)_$(uniqid)_Attribute","rdf:type","sio:attribute","iri"],
    ["this:$(pid)_$(uniqid)_Output","sio:has-value","$(datetime)","xsd:date"]],

  "config" : {
    "source_name" : "source_cde_test",
    "configuration" : "ejp",    
    "csv_name" : "source_1",
    "basicURI" : "this"
    }
}

yarrrml = EMB(data["config"], data["prefixes"],data["triplets"])

test_yarrrml = yarrrml.transform_ShEx()
print(test_yarrrml)
test_shex = yarrrml.transform_YARRRML()
print(test_shex)
test_obda = yarrrml.transform_OBDA()
print(test_obda)
test_sparql = yarrrml.transform_SPARQL()
print(test_sparql)
```
### Documentation:
##### **Configuration parameter**:
* `source_name`: (mandatory for **YARRRML** and **OBDA** representations) used to create each inidividual template object.
* `configuration`: (mandatory for **YARRRML** and **ShEx** representations) used to define a certain workflow to operate. `ejp` in case of custom transformation required to fit with EJP-RD CDE-in-a-box workflow requirements, if not, define as `default`.
* `csv_name`: (mandatory in case of `configuration: default` for **YARRRML** representation) used to define input CSV name. 
* `basicURI`: (mandatory for **ShEx** and **SPARQL** representations) used to identify basic URI prefix to create proper representations. 


### API usage:

This module was implemented as a Web service using FastAPI and Docker to make it run. You can obtain the Docker Image from [Dockerhub](https://hub.docker.com/repository/docker/pabloalarconm/embuilder).

Pull the image `pabloalarconm/embuilder` and run it!

```docker
docker run -p 8000:8000 pabloalarconm/embuilder
```


Its configured to run at your localhost, port 8000. Please check [http://localhost:8000/docs](http://127.0.0.1:8000/docs) to interact with Swagger UI **documentation** of each funcion. You know more about it configuration, here is the [`Dockerfile`](https://github.com/pabloalarconm/EMbuilder/blob/main/Dockerfile) for this implementation.