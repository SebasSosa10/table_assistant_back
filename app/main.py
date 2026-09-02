from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.session import init_db
from user.presentation.router import router as user_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Table Assistant",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(user_router)
