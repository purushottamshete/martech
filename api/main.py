from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.users import router as user_router
from routers.activity_log import router as activity_router
from routers.emails import router as email_router
from routers.plans import router as plan_router
from routers.orders import router as order_router
from routers.apis import router as api_router
from routers.pages import router as page_router
import settings

app = FastAPI()
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(activity_router)
app.include_router(email_router)
app.include_router(plan_router)
app.include_router(order_router)
app.include_router(api_router)
app.include_router(page_router)

app.add_middleware(
    DBSessionMiddleware, 
    db_url=settings.DATABASE_URL)

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
    return {"message": "Welcome to Martech"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)