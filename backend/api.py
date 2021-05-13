import uvicorn
from fastapi import FastAPI
from routers import user

api = FastAPI()
api.include_router(user.router)

@api.get("/")
async def root():
    return {"api": "(￣▽￣)~*"}

if __name__ == '__main__':
    uvicorn.run(api, host="127.0.0.1", port=8008)
