from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db
import os
from typing import Annotated
from fastapi import Depends, FastAPI
from auth import get_current_active_user
from schema import User as UserSchema
from auth import router as auth_router
load_dotenv("../.env")

app = FastAPI()
app.include_router(auth_router)

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

@app.get("/me/", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(get_current_active_user)):
    return current_user

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")