# Task CRUD API

A simple Task Management CRUD API built with **Express.js** and **in-memory storage**. Comes with interactive Swagger docs.

---

## Quick Start

```bash
cd mycrud
npm install
node crud.js
```

Server runs at `http://localhost:3000`

- **Swagger UI:** http://localhost:3000/api-docs

---

## How It Works

The app stores tasks in a plain JavaScript array in memory. Data is lost when the server restarts. It starts pre-loaded with 3 sample tasks:

```js
{ id: 1, title: 'Learn Node.js basics', done: true },
{ id: 2, title: 'Understand Express routing', done: false },
{ id: 3, title: 'Build a CRUD API', done: false }
```

---

## Endpoints

### Info / Health

| Method | Path | What it does | Response |
|--------|------|-------------|----------|
| `GET` | `/` | Welcome message | `"Hello World!"` |
| `GET` | `/api` | API info | `{ name, version, endpoints }` |
| `GET` | `/health` | Health check | `{ status: "ok" }` |

### Tasks

| Method | Path | What it does | Status Codes |
|--------|------|-------------|--------------|
| `GET` | `/tasks` | Get all tasks | 200 |
| `GET` | `/tasks/:id` | Get one task by ID | 200, 404 |
| `POST` | `/tasks` | Create a new task | 201, 400 |
| `PUT` | `/tasks/:id` | Update a task | 200, 400, 404 |
| `DELETE` | `/tasks/:id` | Delete a task | 204, 404 |

---

## Examples

### Get all tasks

```bash
curl http://localhost:3000/tasks
```

```json
[
  { "id": 1, "title": "Learn Node.js basics", "done": true },
  { "id": 2, "title": "Understand Express routing", "done": false },
  { "id": 3, "title": "Build a CRUD API", "done": false }
]
```

### Get one task

```bash
curl http://localhost:3000/tasks/1
```

```json
{ "id": 1, "title": "Learn Node.js basics", "done": true }
```

### Create a task

```bash
curl -X POST http://localhost:3000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy groceries"}'
```

```json
{ "message": "Done, here's your receipt Created: Buy groceries" }
```

> Note: `done` is always set to `false` on creation. The response sends a confirmation message, not the task object.

### Update a task

```bash
curl -X PUT http://localhost:3000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Node.js","done":true}'
```

```json
{ "id": 1, "title": "Learn Node.js", "done": true }
```

You can also send just one field:

```bash
curl -X PUT http://localhost:3000/tasks/2 \
  -H "Content-Type: application/json" \
  -d '{"done":true}'
```

### Delete a task

```bash
curl -X DELETE http://localhost:3000/tasks/3
```

Returns empty body with status 204.

---

## Validation

| Endpoint | Rule | Error |
|----------|------|-------|
| `POST /tasks` | `title` is required | `400 — {"error": "Title is required"}` |
| `PUT /tasks/:id` | At least `title` or `done` must be provided | `400 — {"error": "Empty/Invalid body"}` |
| `GET/PUT/DELETE /tasks/:id` | Task must exist | `404 — {"error": "Task <id> not found"}` |

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `express` | Web framework |
| `swagger-ui-express` | Serves Swagger UI at `/api-docs` |
| `swagger-jsdoc` | (Listed but not used in code) |

---

## Project Files

| File | What it does |
|------|-------------|
| `crud.js` | The entire app — routes, storage, server |
| `swagger.json` | OpenAPI 3.0 spec for Swagger UI |
| `package.json` | Dependencies and project config |
