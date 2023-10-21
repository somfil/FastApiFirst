import uvicorn
from fastapi import FastAPI

from src.auth.routers import router as auth_routers


app = FastAPI()


app.include_router(
    auth_routers,
    tags=['Authentication']
)


if __name__ == '__main__':
    uvicorn.run('main:app')