from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.users.routers import router as users_router
from src.api.products.routers import router as products_router


app = FastAPI(
    title="Test-fullstack",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, tags=["Users"], prefix="/api/users")
app.include_router(products_router, tags=["Products"], prefix="/api/products")
