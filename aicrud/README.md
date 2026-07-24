# FastAPI CRUD API

A complete RESTful CRUD API built with **Python**, **FastAPI**, and **in-memory storage**. Includes pagination, filtering, sorting, search, CORS, and custom error handling.

---

## Quick Start (Under 5 Minutes)

```bash
# 1. Go into the project folder
cd aicrud

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload
```

That's it. The API is now running at `http://127.0.0.1:8000`.

- **Swagger UI (interactive docs):** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc
- **OpenAPI JSON:** http://127.0.0.1:8000/openapi.json

---

## Project Structure

```
aicrud/
├── main.py              # App entry point, CORS, lifespan, OpenAPI override
├── models.py            # Pydantic models (request/response schemas, enums)
├── storage.py           # Thread-safe in-memory storage with auto-increment IDs
├── exceptions.py        # Custom exceptions + global error handlers
├── requirements.txt     # Python dependencies
└── routers/
    ├── __init__.py
    └── items.py         # All API endpoints
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | >=0.115.0 | Web framework |
| `uvicorn[standard]` | >=0.32.0 | ASGI server |
| `pydantic` | >=2.10.0 | Data validation (used by FastAPI) |

---

## API Endpoints

### Health Check

| Method | Path | Status | Description |
|--------|------|--------|-------------|
| `GET` | `/health` | 200 | Returns API status and version |

### Items (CRUD)

| Method | Path | Status Codes | Description |
|--------|------|--------------|-------------|
| `POST` | `/api/items` | **201**, 422 | Create a new item |
| `GET` | `/api/items` | **200** | List items (paginated, filtered, sorted) |
| `GET` | `/api/items/{id}` | **200**, 404 | Get a single item by ID |
| `PUT` | `/api/items/{id}` | **200**, 404, 422 | Fully update an item |
| `DELETE` | `/api/items/{id}` | **204**, 404 | Delete an item |

---

## Request / Response Examples

### Create an Item

```bash
curl -X POST http://127.0.0.1:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Wireless Mouse","description":"Ergonomic mouse","price":29.99,"category":"electronics","in_stock":true}'
```

**201 Response:**
```json
{
  "id": 1,
  "name": "Wireless Mouse",
  "description": "Ergonomic mouse",
  "price": 29.99,
  "category": "electronics",
  "in_stock": true,
  "created_at": "2026-07-24T00:28:38.771707+00:00",
  "updated_at": "2026-07-24T00:28:38.771707+00:00"
}
```

### List Items (with pagination, filtering, sorting, search)

```bash
# Get page 1, 5 items per page, sorted by price ascending
curl "http://127.0.0.1:8000/api/items?skip=0&limit=5&sort_by=price&order=asc"

# Filter by category
curl "http://127.0.0.1:8000/api/items?category=electronics"

# Search for "mouse" in name/description
curl "http://127.0.0.1:8000/api/items?search=mouse"

# Price range filter
curl "http://127.0.0.1:8000/api/items?min_price=10&max_price=50"
```

**200 Response:**
```json
{
  "items": [ { "id": 1, "name": "Wireless Mouse", ... } ],
  "total": 50,
  "skip": 0,
  "limit": 5,
  "has_next": true,
  "has_prev": false
}
```

### Get Single Item

```bash
curl http://127.0.0.1:8000/api/items/1
```

### Update an Item

```bash
curl -X PUT http://127.0.0.1:8000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Wireless Mouse Pro","description":"Updated","price":39.99,"category":"electronics","in_stock":false}'
```

### Delete an Item

```bash
curl -X DELETE http://127.0.0.1:8000/api/items/1
```

---

## Query Parameters (List Endpoint)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | int | `0` | Number of records to skip |
| `limit` | int | `10` | Max records per page |
| `category` | string | `null` | Filter by category (`electronics`, `clothing`, `food`, `other`) |
| `in_stock` | boolean | `null` | Filter by stock status |
| `min_price` | float | `null` | Minimum price |
| `max_price` | float | `null` | Maximum price |
| `search` | string | `null` | Case-insensitive search in name and description |
| `sort_by` | string | `created_at` | Sort field: `created_at`, `price`, or `name` |
| `order` | string | `desc` | Sort direction: `asc` or `desc` |

---

## Validation Rules

| Field | Type | Rules |
|-------|------|-------|
| `name` | string | Required, 1–100 characters |
| `description` | string | Optional, max 500 characters |
| `price` | float | Required, must be > 0 |
| `category` | string | Required, one of: `electronics`, `clothing`, `food`, `other` |
| `in_stock` | boolean | Optional, defaults to `true` |

---

## Error Responses

| Status | When | Response |
|--------|------|----------|
| 404 | Item not found | `{"detail": "Item not found (id=5)"}` |
| 422 | Validation error | `{"detail": "Validation error"}` |
| 500 | Unexpected error | `{"detail": "Internal server error"}` |

---

## Features

- **In-memory storage** with auto-incrementing IDs (no database needed)
- **Thread-safe** storage layer using `threading.Lock`
- **Pagination** with `total`, `has_next`, `has_prev` metadata
- **Filtering** by category, stock status, and price range
- **Search** — case-insensitive substring match across name and description
- **Sorting** by any field, ascending or descending
- **CORS** — allows all origins (restrict in production)
- **Custom OpenAPI** — Schemas section hidden from Swagger UI
- **Lifespan events** — startup/shutdown hooks via FastAPI's `asynccontextmanager`

---

## Data Model

```json
{
  "id": 1,
  "name": "string",
  "description": "string | null",
  "price": 9.99,
  "category": "electronics | clothing | food | other",
  "in_stock": true,
  "created_at": "2026-07-24T00:28:38.771707+00:00",
  "updated_at": "2026-07-24T00:28:38.771707+00:00"
}
```
