from fastapi import FastAPI
from pydantic import BaseModel
from builder import EMB
from data.test import prefixes, triplets, config
from fastapi import FastAPI , Response
# from pydantic import BaseModel
# from starlette.requests import Request
# import yaml


app = FastAPI()

@app.post("/yarrrml/")
async def transform(): 
    test = EMB(config, prefixes, triplets)
    data = test.transform_YARRRML()
    return  data


@app.post("/obda/")
async def transform():
    test = EMB(config, prefixes, triplets)
    data = test.transform_OBDA()
    return  data