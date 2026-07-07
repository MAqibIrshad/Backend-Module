"Pause this function until this task finishes, but let the server work on other requests in the meantime."
from fastapi import FastAPI
from database import create_db_tables
from contextlib import asynccontextmanager
from routers.tasks import task_router
from routers.users import user_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield
    

app = FastAPI(lifespan=lifespan)
# tasks = []
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(user_router)

    