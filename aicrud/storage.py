"""
In-memory storage layer with auto-incrementing IDs.
Simulates a database using Python dictionaries.
"""

from __future__ import annotations

import threading
from datetime import datetime, timezone
from typing import Any, Optional


class InMemoryStorage:
    """Thread-safe in-memory key-value store with auto-incrementing integer IDs."""

    def __init__(self) -> None:
        self._store: dict[int, dict[str, Any]] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """Insert a new record. Returns the record with auto-generated id and timestamps."""
        with self._lock:
            now = datetime.now(timezone.utc).isoformat()
            record = {
                "id": self._next_id,
                **data,
                "created_at": now,
                "updated_at": now,
            }
            self._store[self._next_id] = record
            self._next_id += 1
            return record.copy()

    def get(self, record_id: int) -> Optional[dict[str, Any]]:
        """Retrieve a single record by ID, or None if not found."""
        record = self._store.get(record_id)
        return record.copy() if record else None

    def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[dict[str, Any]] = None,
        search_fields: Optional[list[str]] = None,
        search_term: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "asc",
    ) -> tuple[list[dict[str, Any]], int]:
        """
        Retrieve records with pagination, filtering, search, and sorting.

        Returns (items, total_count) where total_count is the count before pagination.
        """
        items = list(self._store.values())

        # --- Filtering ---
        if filters:
            for key, value in filters.items():
                if value is not None:
                    items = [r for r in items if r.get(key) == value]

        # --- Price range (special filters) ---
        # Handled in the router; here we accept min_price / max_price via filters dict
        min_price = filters.get("min_price") if filters else None
        max_price = filters.get("max_price") if filters else None
        if min_price is not None:
            items = [r for r in items if r.get("price", 0) >= min_price]
        if max_price is not None:
            items = [r for r in items if r.get("price", 0) <= max_price]

        # --- Search ---
        if search_term and search_fields:
            term = search_term.lower()
            items = [
                r for r in items
                if any(term in str(r.get(f, "")).lower() for f in search_fields)
            ]

        total = len(items)

        # --- Sorting ---
        if sort_by:
            reverse = sort_order.lower() == "desc"
            items.sort(key=lambda r: r.get(sort_by, ""), reverse=reverse)

        # --- Pagination ---
        items = items[skip : skip + limit]

        return [r.copy() for r in items], total

    def update(self, record_id: int, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Update an existing record. Returns the updated record or None."""
        with self._lock:
            existing = self._store.get(record_id)
            if existing is None:
                return None
            existing.update(data)
            existing["updated_at"] = datetime.now(timezone.utc).isoformat()
            return existing.copy()

    def delete(self, record_id: int) -> bool:
        """Delete a record. Returns True if deleted, False if not found."""
        with self._lock:
            return self._store.pop(record_id, None) is not None

    def count(self, **kwargs: Any) -> int:
        """Return total number of records (ignores filters — use get_all for filtered count)."""
        return len(self._store)


# Singleton instance shared across the app
items_storage = InMemoryStorage()
