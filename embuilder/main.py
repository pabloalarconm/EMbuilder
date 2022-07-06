from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import yaml

from embuilder.builder import EMB
from pydantic import BaseModel

class Datainput(BaseModel):
    config: dict
    prefixes: dict
    triplets: list


app = FastAPI()

@app.get("/")
async def index():
    return {"API":"Running"}

@app.post("/yarrrml/")
async def yarrrml_transformation(Input: Datainput): 
    """
    * Obtain YARRRML using a single JSON object with all prefixes, triplets and configuration parameter.

    * Exemplar JSON data for this call cand be found at this [Github](https://github.com/pabloalarconm/EMbuilder/tree/main/embuilder/data) repo. 

    ```python {
        "config": {},

        "prefixes": {},

        "triplets": [
            ["Subject", "Predicate", "Object", "Datatype"],
            ["Subject", "Predicate", "Object", "Datatype"],
            ...
            ]
        }
    ``` 
    """
    test = EMB(config=Input.config, prefixes=Input.prefixes, triplets=Input.triplets)
    yaml_raw = test.transform_YARRRML()
    json_yaml = yaml.safe_load(yaml_raw)
    result_yaml = yaml.dump(json_yaml, indent=2, allow_unicode=True, encoding="utf8")
    return PlainTextResponse(content=result_yaml, media_type='text/x-yaml')

@app.post("/obda/",response_class=PlainTextResponse)
async def obda_transformation(Input: Datainput):
    """
    * Obtain OBDA (Ontology based Database Access) using a single JSON object with all prefixes, triplets and configuration parameter.

    * Exemplar JSON data for this call cand be found at this [Github](https://github.com/pabloalarconm/EMbuilder/tree/main/embuilder/data) repo. 

    ```python {
        "config": {},

        "prefixes": {},

        "triplets": [
            ["Subject", "Predicate", "Object", "Datatype"],
            ["Subject", "Predicate", "Object", "Datatype"],
            ...
            ]
        }
    ``` 
    """
    test = EMB(config=Input.config, prefixes=Input.prefixes, triplets=Input.triplets)
    data = test.transform_OBDA()
    return PlainTextResponse(content=data, media_type='text')

@app.post("/shex/",response_class=PlainTextResponse)
async def shex_transformation(Input: Datainput):
    """
    * Obtain ShEx (Shape Expression) using a single JSON object with all prefixes, triplets and configuration parameter.

    * Exemplar JSON data for this call cand be found at this [Github](https://github.com/pabloalarconm/EMbuilder/tree/main/embuilder/data) repo. 

    ```python {
        "config": {},

        "prefixes": {},

        "triplets": [
            ["Subject", "Predicate", "Object", "Datatype"],
            ["Subject", "Predicate", "Object", "Datatype"],
            ...
            ]
        }
    ``` 
    """
    test = EMB(config=Input.config, prefixes=Input.prefixes, triplets=Input.triplets)
    data = test.transform_ShEx()
    return PlainTextResponse(content=data, media_type='text')

@app.post("/sparql/",response_class=PlainTextResponse)
async def sparql_transformation(Input: Datainput):
    """
    * Obtain SPARQL query using a single JSON object with all prefixes, triplets and configuration parameter.

    * Exemplar JSON data for this call cand be found at this [Github](https://github.com/pabloalarconm/EMbuilder/tree/main/embuilder/data) repo. 

    ```python {
        "config": {},

        "prefixes": {},

        "triplets": [
            ["Subject", "Predicate", "Object", "Datatype"],
            ["Subject", "Predicate", "Object", "Datatype"],
            ...
            ]
        }
    ``` 
    """
    test = EMB(config=Input.config, prefixes=Input.prefixes, triplets=Input.triplets)
    data = test.transform_SPARQL()
    return PlainTextResponse(content=data, media_type='text')