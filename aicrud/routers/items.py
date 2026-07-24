"""
CRUD endpoints for the Items resource + Health check.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Query, Response, status

from exceptions import NotFoundException
from storage import items_storage

router = APIRouter(tags=["Items"])


def _get_or_404(item_id: int) -> dict:
    item = items_storage.get(item_id)
    if item is None:
        raise NotFoundException("Item", item_id)
    return item


@router.get("/health", summary="Health check")
def health_check() -> dict:
    return {"status": "healthy", "version": "1.0.0"}


@router.post(
    "/api/items",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
)
def create_item(body: dict) -> dict:
    return items_storage.create(body)


@router.get(
    "/api/items",
    summary="List items with pagination, filtering, and sorting",
)
def list_items(
    skip: int = Query(0),
    limit: int = Query(10),
    category: Optional[str] = Query(None),
    in_stock: Optional[bool] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("created_at"),
    order: Optional[str] = Query("desc"),
) -> dict:
    filters: dict = {}
    if category is not None:
        filters["category"] = category
    if in_stock is not None:
        filters["in_stock"] = in_stock
    if min_price is not None:
        filters["min_price"] = min_price
    if max_price is not None:
        filters["max_price"] = max_price

    items, total = items_storage.get_all(
        skip=skip,
        limit=limit,
        filters=filters if filters else None,
        search_fields=["name", "description"],
        search_term=search,
        sort_by=sort_by,
        sort_order=order,
    )

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "has_next": skip + limit < total,
        "has_prev": skip > 0,
    }


@router.get(
    "/api/items/{item_id}",
    summary="Get a single item by ID",
)
def get_item(item_id: int) -> dict:
    return _get_or_404(item_id)


@router.put(
    "/api/items/{item_id}",
    summary="Update an item",
)
def update_item(item_id: int, body: dict) -> dict:
    _get_or_404(item_id)
    return items_storage.update(item_id, body)


@router.delete(
    "/api/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
    response_class=Response,
)
def delete_item(item_id: int) -> Response:
    _get_or_404(item_id)
    items_storage.delete(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
