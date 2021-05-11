import uvicorn
from fastapi import FastAPI
from backend.routers import user

api = FastAPI()
api.include_router(user.router)

@api.get("/")
async def root():
    return {"api": "(￣▽￣)~*"}