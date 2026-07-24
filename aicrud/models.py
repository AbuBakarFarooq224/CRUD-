"""
Pydantic models for request validation and response schemas.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ItemCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"
    other = "other"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class SortField(str, Enum):
    created_at = "created_at"
    price = "price"
    name = "name"


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    category: ItemCategory
    in_stock: bool = True


class ItemUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    category: ItemCategory
    in_stock: bool = True


# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    category: ItemCategory
    in_stock: bool
    created_at: str
    updated_at: str


class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_prev: bool


class ErrorResponse(BaseModel):
    detail: str
    code: str | None = None


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "1.0.0"
