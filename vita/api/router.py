from dotenv import load_dotenv
from fastapi import FastAPI

from vita.api.routers import health_router

load_dotenv()
vita = "vita".upper()
app = FastAPI(title=vita, version="0.1.0")

app.include_router(health_router.router, tags=["health"])
