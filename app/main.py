from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from request import RequestModel
from pydantic import BaseModel

DATABASE_URL = "postgresql://root:root@db:5432/postgres"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

class User(BaseModel):
    name: str
    gender: str
    height: float
    birth_place: str

app = FastAPI()

metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/hello")
async def greetings():
    return {
        "message": "Hello World."
    }

@app.post("/echo/")
async def parrot_response(request_data: RequestModel):
    input_message = request_data.message
    response_content = {
        "content": input_message
        }
    return response_content

@app.get("/hoge")
async def loadfile(file):
    with open('hoge.txt') as h:
        h.seek(0)
        text = h.read()
    return {
        "content": text
    }

# @app.on_event("startup")
# async def startup():
#     # Start up the app
#     app.state.db = SessionLocal()

# @app.on_event("shutdown")
# async def shutdown():
#     # Close db connection (if used with an async engine)
#     app.state.db.close()

@app.post("/users/")
async def create_user(name: str, email: str):
    # Create a new user
    with app.state.db.begin() as transaction:
        transaction.execute(users.insert().values(name=name, email=email))

@app.get("/users/")
async def read_users():
    # Read all users
    with app.state.db.begin() as transaction:
        result = transaction.execute(select([users]))
        return result.fetchall()


# from fastapi import FastAPI
# from pydantic import BaseModel
# from sqlalchemy import create_engine, Table, MetaData
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://postgres:postgres@db:5432/test_db"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# metadata = MetaData()
# people = Table('people', metadata, autoload_with=engine)

# app = FastAPI()

# class Person(BaseModel):
#     name: str
#     gender: str
#     height: float
#     birthplace: str

# @app.post("/people/")
# def create_person(person: Person):
#     with SessionLocal() as session:
#         result = session.execute(people.insert().values(
#             name=person.name,
#             gender=person.gender,
#             height=person.height,
#             birthplace=person.birthplace
#         ))
#         session.commit()
#         return {"id": result.inserted_primary_key[0]}