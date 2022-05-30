# **EMbuilder** 
## **Etemenanki Builder**

Python3 based template builder for Semantic Web transformation:
* [**YARRRML** (YAML -based RDF Mapping Language)](https://rml.io/yarrrml/spec/)
* **OBDA** (Ontology Based Database Acccess)
* [**ShEx** (Shape Expression)](http://shex.io/shex-semantics/index.html)

### **Instalation:** 
Install it locally using ```python3 setup.py install``` or using Pypi repository.

```
pip install EMbuilder
```
### **Example:** 
Use [trial.py](https://github.com/pabloalarconm/EMbuilder/blob/main/trial.py) as a use case for creating your templates:

```python
from embuilder.builder import EMB

prefixes = dict(
  rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#" ,
  rdfs = "http://www.w3.org/2000/01/rdf-schema#" ,
  obo = "http://purl.obolibrary.org/obo/" ,
  sio = "http://semanticscience.org/resource/" ,
  xsd = "http://www.w3.org/2001/XMLSchema#",
  this = "http://my_example.com/")


triplets = [

# sio nodes
["this:$(pid)_$(uniqid)_ID","sio:denotes","this:$(pid)_$(uniqid)_Role","iri"],
["this:$(pid)_$(uniqid)_Entity","sio:has-role","this:$(pid)_$(uniqid)_Role","iri"],
["this:$(pid)_$(uniqid)_Role","sio:is-realized-in","this:$(pid)_$(uniqid)_Process","iri"],
["this:$(pid)_$(uniqid)_Process","sio:has-output","this:$(pid)_$(uniqid)_Output","iri"],
["this:$(pid)_$(uniqid)_Output","sio:refers-to","this:$(pid)_$(uniqid)_Attribute","iri"],
["this:$(pid)_$(uniqid)_Entity","sio:has-attribute","this:$(pid)_$(uniqid)_Attribute","iri"],

# sio types
["this:$(pid)_$(uniqid)_ID","rdf:type","sio:identifier","iri"],
["this:$(pid)_$(uniqid)_Entity","rdf:type","sio:person","iri"],
["this:$(pid)_$(uniqid)_Role","rdf:type","sio:role","iri"],
["this:$(pid)_$(uniqid)_Process","rdf:type","sio:process","iri"],
["this:$(pid)_$(uniqid)_Output","rdf:type","sio:information-content-entity","iri"],
["this:$(pid)_$(uniqid)_Attribute","rdf:type","sio:attribute","iri"],

# data
["this:$(pid)_$(uniqid)_Output","sio:has-value","$(datetime)","xsd:date"]]



config = dict(
  source_name = "source_cde_test",
  configuration = "ejp",    # Two options for this parameter:
                            # ejp: it defines CDE-in-a-Box references, being compatible with this workflow  
                            # csv: No workflow defined, set the source configuration for been used by CSV as data source
                            
  csv_name = "source_1" # parameter only needed in case you pick "csv" as configuration
)

build = EMB(config, prefixes,triplets)

test = build.transform_ShEx("this") # Define your basic URI as a parameter
test2 = build.transform_YARRRML()
test3 = build.transform_OBDA()


print(test)
print(test2)
print(test3)
```