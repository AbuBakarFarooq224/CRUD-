# SWAGGERUI CRUD API

A CRUD API for items built with **SWAGGERUI** and **in-memory storage**.

---

## Quick Start

```bash
cd aicrud
pip install -r requirements.txt
uvicorn main:app --reload
```

Server runs at `http://127.0.0.1:8000`

- **Swagger UI:** http://127.0.0.1:8000/docs

---

## Endpoints

| Method | Path | What it does | Status Codes |
|--------|------|-------------|--------------|
| `GET` | `/health` | Health check | 200 |
| `POST` | `/api/items` | Create an item | 201, 422 |
| `GET` | `/api/items` | List items (filtered, sorted, paginated) | 200 |
| `GET` | `/api/items/{id}` | Get one item | 200, 404 |
| `PUT` | `/api/items/{id}` | Update an item | 200, 404 |
| `DELETE` | `/api/items/{id}` | Delete an item | 204, 404 |

---

## Examples

### Create an item

```bash
curl -X POST http://127.0.0.1:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Wireless Mouse","price":29.99,"category":"electronics"}'
```

```json
{
  "id": 1,
  "name": "Wireless Mouse",
  "description": null,
  "price": 29.99,
  "category": "electronics",
  "in_stock": true,
  "created_at": "2026-07-24T00:28:38.771Z",
  "updated_at": "2026-07-24T00:28:38.771Z"
}
```

### Get all items

```bash
curl http://127.0.0.1:8000/api/items
```

```json
{
  "items": [...],
  "total": 3,
  "skip": 0,
  "limit": 10,
  "has_next": false,
  "has_prev": false
}
```

### Get one item

```bash
curl http://127.0.0.1:8000/api/items/1
```

### Update an item

```bash
curl -X PUT http://127.0.0.1:8000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Wireless Mouse Pro","price":39.99,"category":"electronics","in_stock":false}'
```

### Delete an item

```bash
curl -X DELETE http://127.0.0.1:8000/api/items/1
```

---

## Query Parameters (GET /api/items)

| Param | Type | Default | What it does |
|-------|------|---------|-------------|
| `skip` | int | 0 | How many to skip |
| `limit` | int | 10 | How many to return |
| `category` | string | - | Filter by category |
| `in_stock` | bool | - | Filter by stock |
| `min_price` | float | - | Minimum price |
| `max_price` | float | - | Maximum price |
| `search` | string | - | Search name/description |
| `sort_by` | string | `created_at` | Sort field |
| `order` | string | `desc` | `asc` or `desc` |

---

## Project Files

| File | What it does |
|------|-------------|
| `main.py` | App entry point, CORS, OpenAPI setup |
| `routers/items.py` | All API routes |
| `models.py` | Pydantic schemas |
| `storage.py` | In-memory data store |
| `exceptions.py` | Error handling |
| `requirements.txt` | Dependencies |
