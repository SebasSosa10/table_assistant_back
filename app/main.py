from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import init_db
from conversation.presentation.router import router as conversation_router
from restaurant.presentation.router import router as restaurant_router
from shared.config.settings import settings
from table.presentation.router import router as table_router
from user.presentation.deps import get_current_user
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(
    restaurant_router,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    table_router,
    dependencies=[Depends(get_current_user)],
)
app.include_router(
    conversation_router,
    dependencies=[Depends(get_current_user)],
)
