from fastapi import FastAPI
from router import user_router, post_router, login_router
from fastapi.middleware.cors import CORSMiddleware
from schema.database import initialize_database
from contextlib import asynccontextmanager


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database() # startup code
    yield
    # optional: cleanup code below in async function

app = FastAPI(lifespan=lifespan)
app.include_router(user_router.route)
app.include_router(post_router.route)
app.include_router(login_router.route)


