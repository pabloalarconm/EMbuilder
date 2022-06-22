from fastapi import FastAPI
from pydantic import BaseModel
from builder import EMB
#from os import listdir, getcwd
from data.test import prefixes, triplets, config
from fastapi import FastAPI , Response
#from pydantic import BaseModel
# from starlette.requests import Request
import yaml


# openapi_extra={
#   "200": {
#     "content": {
#       "application/yaml": {
#         "schema": YARRRML.schema()
#       }
#     }
#   }}


app = FastAPI()

# class YARRRML(BaseModel):
#     prefixes : dict
#     mapping : dict
#     source : dict



@app.post("/yarrrml/"
# ,openapi_extra={
#   "200": {
#     "content": "application/yaml"
#     }
#   }
)
async def transform():# response: Response
    # request Headers:

    # Response Headers
    # del response.headers["accept"] 
    # del response.headers["content-type"]
    # response.headers["Accept"] = "application/yaml" 
    # response.headers["Content-Type"] = "application/yaml; charset=utf-8"

    test = EMB(config, prefixes, triplets)
    data = test.transform_YARRRML()
    #result = yaml.safe_load(data)
    return  data

# @app.get("/")
# def get_yaml(response: Response):
#     response.headers["Accept"] = "application/yaml" 
#     response.headers["Content-Type"] = "application/yaml; charset=utf-8"



@app.post("/obda/") # response_model=OBDA
async def transform():# response: Response
    # request Headers:

    # Response Headers
    # del response.headers["accept"] 
    # del response.headers["content-type"]
    # response.headers["Accept"] = "text" 
    # response.headers["Content-Type"] = "text; charset=utf-8"

    test = EMB(config, prefixes, triplets)
    data = test.transform_OBDA()
    #result = yaml.safe_load(data)
    return  data

@app.post("/shex/")
async def transform():# response: Response
    # request Headers:

    # Response Headers
    # del response.headers["accept"] 
    # del response.headers["content-type"]
    # response.headers["Accept"] = "application/yaml" 
    # response.headers["Content-Type"] = "application/yaml; charset=utf-8"

    test = EMB(config, prefixes, triplets)
    data = test.transform_ShEx("this")
    #result = yaml.safe_load(data)
    return  data


@app.post("/sparql/")
async def transform():# response: Response
    # request Headers:

    # Response Headers
    # del response.headers["accept"] 
    # del response.headers["content-type"]
    # response.headers["Accept"] = "application/yaml" 
    # response.headers["Content-Type"] = "application/yaml; charset=utf-8"

    test = EMB(config, prefixes, triplets)
    data = test.transform_SPARQL("this")
    #result = yaml.safe_load(data)
    return  data
    

