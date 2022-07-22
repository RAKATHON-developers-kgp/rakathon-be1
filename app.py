import logging
import typing 
from fastapi import FastAPI, Request, routing
from requests import request
# from pydantic.fields import FieldInfo, Undefined
import database.mysqldb as db
import database.basemodels as bm
from fastapi.middleware.cors import CORSMiddleware


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

