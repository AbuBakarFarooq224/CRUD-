"""
FastAPI CRUD API — Main Application Entry Point.

Run with:
    uvicorn main:app --reload
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from exceptions import register_exception_handlers
from routers.items import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("🚀 API is starting up...")
    yield
    print("🛑 API is shutting down...")


app = FastAPI(
    title="FastAPI CRUD API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(items_router)


# Strip the Schemas section from Swagger UI
_original_openapi = app.openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = _original_openapi()
    schema.pop("components", None)
    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi
