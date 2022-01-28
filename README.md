# **EMbuilder** -- **Etemenanki Builder**
### Python-controlled YARRRML builder for creating YAML based RML templates using Python.

### **Instalation:** install locally or using Pypi repository.

```
python3 setup.py install
```

```
pip install EMbuilder
```
### **Example:** 
### Use [trial.py](https://github.com/pabloalarconm/EMbuilder/blob/main/trial.py) as a trial for creating your templates:

```python
from embuilder.builder import EMB

prefixes = dict(
  rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#" ,
  rdfs = "http://www.w3.org/2000/01/rdf-schema#" ,
  obo = "http://purl.obolibrary.org/obo/" ,
  sio = "http://semanticscience.org/resource/" ,
  dc = "http://purl.org/dc/elements/1.1/",
  this = "http://my_example.com/")


triplets = [

# sio nodes
["this:$(pid)_$(uniqid)#ID","sio:denotes","this:$(pid)_$(uniqid)#Role","iri"],
["this:$(pid)_$(uniqid)#Entity","sio:has-role","this:$(pid)_$(uniqid)#Role","iri"],
["this:$(pid)_$(uniqid)#Role","sio:is-realized-in","this:$(pid)_$(uniqid)#Process","iri"],
["this:$(pid)_$(uniqid)#Process","sio:has-output","this:$(pid)_$(uniqid)#Output","iri"],
["this:$(pid)_$(uniqid)#Output","sio:refers-to","this:$(pid)_$(uniqid)#Attribute","iri"],
["this:$(pid)_$(uniqid)#Entity","sio:has-attribute","this:$(pid)_$(uniqid)#Attribute","iri"],

# sio types
["this:$(pid)_$(uniqid)#ID","rdf:type","sio:identifier","iri"],
["this:$(pid)_$(uniqid)#Entity","rdf:type","sio:person","iri"],
["this:$(pid)_$(uniqid)#Role","rdf:type","sio:role","iri"],
["this:$(pid)_$(uniqid)#Process","rdf:type","sio:process","iri"],
["this:$(pid)_$(uniqid)#Output","rdf:type","sio:information-content-entity","iri"],
["this:$(pid)_$(uniqid)#Attribute","rdf:type","sio:attribute","iri"],

# data
["this:$(pid)_$(uniqid)#Output","sio:has-value","$(datetime)","xsd:date"]]



config = dict(
  source_name = "source_cde_test",
  configuration = "ejp",    # Two options for this parameter:
                            # ejp: it defines CDE-in-a-Box references, being compatible with this workflow  
                            # csv: No workflow defined, set the source configuration for been used by CSV as data source
                            
  csv_name = "source_1" # parameter only needed in case you pick "csv" as configuration
)

yarrrml = EMB(config)
test = yarrrml.transform(prefixes, triplets)
print(test)
```