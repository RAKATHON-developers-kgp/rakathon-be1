import logging
import typing 
from fastapi import FastAPI, Request, routing
from requests import request
# from pydantic.fields import FieldInfo, Undefined
import database.mysqldb as db
import database.basemodels as bm
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os


logging.basicConfig(
    level=logging.INFO,
    # format="{asctime} {name} {levelname:<8} log:{message}",
    format= '%(asctime)s %(name)s %(levelname)s:%(message)s',

    # style="{",
    filename="sample_logs_app.log",
    filemode='w'
    )


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_data")
def scan():
    try:
        listt = db.get_data()
        logging.info("endpoint: '/get_data' , Task executed succesfully")
    except:
        error_statement = "Something went wrong with endpoint: /get_data"
        logging.error(error_statement)
        return error_statement
    return listt


@app.post("/input_name")
async def input(request: Request):
    # data = dict(data)
    # data = dict(request.query_params)
    request = await request.json()
    try:
        name = request.get('name', 'nothing1')
        print(name)
        db.input_data(name)
        logging.info("endpoint: '/input_name' , added name succesfully")

    except:
        error_statement = "Something is wrong with your input at endpoint: /input_name"
        logging.error(error_statement)
        return error_statement

@app.delete("/delete_data")
async def delete(request: Request):
    # data = dict(data)
    request = await request.json()

    try:
        name = request.get('name')
        db.delete_data(name)
        logging.info("endpoint: '/delete_data' , deleted name succesfully")
    except:
        error_statement = "Something is wrong with your input at endpoint: /delete_data"
        logging.error(error_statement)
        return error_statement


load_dotenv()

URL = os.getenv('URL')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD') 

def configuration():

    es = Elasticsearch(
        URL,
        http_auth=(USER, PASSWORD)
    )
    return es


@app.post("/query_data")
async def query(request:Request):
    # request = {
    #     "must":['Task'],
    #     "should":['Task'],
    #     "not":['uvicorn.error']
    # }

    es = configuration()
    s1 = Search(using=es, index = "app.logs-*")


    request = await request.json()
    print(request)
    request1 = request.get('formField4')
    # print(request, 'happyyy')

    print(request1, "jaibambam")

    # print("requets dataa", request.json)

    must_params = request1.get('must', ['null'])
    must_not_params = request1.get('not', ['null'])
    should_params = request1.get('should', ['null'])
    filter = request1.get('filter', 'nothing')
    # filter = filter.get('0', 'nothing')
    re_filter = filter.get('0')
    print(type(must_params), 'jajajaja')

    limit = json.loads(request1.get('limit', '0'))
    offset = json.loads(request1.get('offset', '10'))
    print((offset))

    # if offset == '10':
    #     offset = 10

    must_query =[]
    # print(must_params[0])
    if must_params[0] != '':
        for i in must_params:
            q = Q('match',  message = i )
            must_query.insert(0,q)

    must_not_query=[]
    if must_not_params[0] != '':
        for i in must_not_params:
            q = Q('match',  message = i )
            must_not_query.insert(0,q)

    should_query = []
    # print(type(should_params[0]))

    if should_params[0] != '':
        for i in should_params:
            q = Q('match',  message = i )
            should_query.insert(0,q) 

    a = re_filter.get('lte', int((datetime.now().timestamp())*1000))
    b = re_filter.get('gte', int((datetime.now() - timedelta(minutes = 100000)).timestamp())*1000)
    if a == '' and b == '':
        a = int((datetime.now().timestamp())*1000)
        b = int((datetime.now() - timedelta(minutes = 10000)).timestamp())*1000
    date_filter = { "range": { "@timestamp": { "format": "epoch_millis", "gte": int(b), "lte": int(a) } } }
    q = Q('bool', must = must_query, must_not = must_not_query , should = should_query, filter = date_filter)

    s1.query = q
    s1 = s1[limit:offset]
    res = s1.execute().to_dict()['hits']['hits']
    # print(res)

    final_res =[]
    for i in res:
        index = i.get('_index')
        id = i.get('_id')
        timestamp = i['_source'].get('@timestamp')
        message = i['_source'].get('message')
        path = i['_source']['log']['file'].get('path')
        dict = {'index':index, 'id':id, 'timestamp': timestamp, 'log': message, 'path':path}
        final_res.append(dict)

    return final_res

