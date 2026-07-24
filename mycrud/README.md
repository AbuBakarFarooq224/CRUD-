# Express CRUD API

A complete RESTful CRUD API built with **Node.js**, **Express**, and **in-memory storage**. Includes API key authentication, rate limiting, pagination, filtering, sorting, search, CORS, and custom error handling.

---

## Quick Start (Under 5 Minutes)

```bash
# 1. Go into the project folder
cd mycrud

# 2. Install dependencies
npm install

# 3. Start the server
npm start
```

That's it. The API is now running at `http://localhost:3000`.

- **Health check:** http://localhost:3000/api/health

> **Note:** All endpoints (except health check) require an `x-api-key` header. The default key is set in the `.env` file.

---

## Project Structure

```
mycrud/
├── app.js           # Express app — all routes, middleware, storage
├── package.json     # Node.js dependencies and scripts
├── .env             # Environment variables (PORT, API_KEY)
└── node_modules/    # Installed dependencies
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `express` | Web framework |
| `dotenv` | Loads `.env` file into `process.env` |

---

## Environment Variables (.env)

```env
PORT=3000
API_KEY=your_api_key_here
```

Change `API_KEY` to any secret string. All requests must include this key in the `x-api-key` header.

---

## API Endpoints

### Health Check

| Method | Path | Status | Auth | Description |
|--------|------|--------|------|-------------|
| `GET` | `/api/health` | 200 | No | Returns API status and version |

### Items (CRUD)

| Method | Path | Status Codes | Auth | Description |
|--------|------|--------------|------|-------------|
| `POST` | `/api/items` | **201**, 400, 401 | Yes | Create a new item |
| `GET` | `/api/items` | **200** | Yes | List items (paginated, filtered, sorted) |
| `GET` | `/api/items/:id` | **200**, 404 | Yes | Get a single item by ID |
| `PUT` | `/api/items/:id` | **200**, 400, 404 | Yes | Fully update an item |
| `PATCH` | `/api/items/:id` | **200**, 404 | Yes | Partially update an item |
| `DELETE` | `/api/items/:id` | **204**, 404 | Yes | Delete an item |

---

## Authentication

Every request (except `/api/health`) must include the API key header:

```
x-api-key: your_api_key_here
```

**Missing or wrong key returns:**
```
401 Unauthorized — {"error": "Invalid or missing API key"}
```

---

## Rate Limiting

- **100 requests per 15 minutes** per IP address
- Exceeding the limit returns:
```
429 Too Many Requests — {"error": "Too many requests, please try again later"}
```

---

## Request / Response Examples

### Create an Item

```bash
curl -X POST http://localhost:3000/api/items \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_api_key_here" \
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
  "created_at": "2026-07-24T00:28:38.771Z",
  "updated_at": "2026-07-24T00:28:38.771Z"
}
```

### List Items (with pagination, filtering, sorting, search)

```bash
# Page 1, 5 items per page, sorted by price ascending
curl "http://localhost:3000/api/items?skip=0&limit=5&sort_by=price&order=asc" \
  -H "x-api-key: your_api_key_here"

# Filter by category
curl "http://localhost:3000/api/items?category=electronics" \
  -H "x-api-key: your_api_key_here"

# Search in name/description
curl "http://localhost:3000/api/items?search=mouse" \
  -H "x-api-key: your_api_key_here"

# Price range
curl "http://localhost:3000/api/items?min_price=10&max_price=50" \
  -H "x-api-key: your_api_key_here"
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
curl http://localhost:3000/api/items/1 \
  -H "x-api-key: your_api_key_here"
```

### Update an Item (PUT — all fields required)

```bash
curl -X PUT http://localhost:3000/api/items/1 \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_api_key_here" \
  -d '{"name":"Wireless Mouse Pro","description":"Updated","price":39.99,"category":"electronics","in_stock":false}'
```

### Partial Update (PATCH — only send what you want to change)

```bash
curl -X PATCH http://localhost:3000/api/items/1 \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_api_key_here" \
  -d '{"price":34.99}'
```

### Delete an Item

```bash
curl -X DELETE http://localhost:3000/api/items/1 \
  -H "x-api-key: your_api_key_here"
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

### Create (POST) & Full Update (PUT)

| Field | Rules |
|-------|-------|
| `name` | Required — cannot be empty |
| `price` | Required — must be a number > 0 |
| `category` | Optional — string |
| `description` | Optional — string |
| `in_stock` | Optional — boolean, defaults to `true` |

### Partial Update (PATCH)

No validation — accepts any subset of fields.

---

## Error Responses

| Status | When | Response |
|--------|------|----------|
| 400 | Missing name/price or invalid price | `{"error": "Name is required"}` or `{"error": "Price must be a number greater than 0"}` |
| 401 | Missing or invalid API key | `{"error": "Invalid or missing API key"}` |
| 404 | Item not found | `{"error": "Item not found"}` |
| 429 | Rate limit exceeded | `{"error": "Too many requests, please try again later"}` |

---

## Development

```bash
# Start with auto-reload (nodemon)
npm run dev
```

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
  "created_at": "2026-07-24T00:28:38.771Z",
  "updated_at": "2026-07-24T00:28:38.771Z"
}
```
