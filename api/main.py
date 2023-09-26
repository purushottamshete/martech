from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db
import os

load_dotenv(".env")

app = FastAPI()

app.add_middleware(
    DBSessionMiddleware, 
    db_url=os.environ['DATABASE_URL'])

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")