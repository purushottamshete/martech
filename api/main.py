from fastapi import FastAPI, Request, status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.responses import JSONResponse
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
import logging
import time
from uuid import uuid4

logging.config.fileConfig('logging.conf', defaults={'logfilename': settings.LOG_FILE})
logger = logging.getLogger('routers')

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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = str(uuid4())
    logger.debug(f"rid={idem} start request method={request.method} path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.debug(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response

@app.get("/")
def root():
    return JSONResponse(content={"message": "Welcome to Martech"})

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)