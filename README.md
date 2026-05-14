# 📦 Inventory Management API

A RESTful API built with **FastAPI** and **MongoDB Atlas** for managing inventory items. Supports creating items with unique name enforcement and fetching items by either their ID or name. JWT-based authentication is also wired in for route protection.

---

## 🛠️ Tech Stack

| Layer        | Technology              |
|-------------|------------------------|
| Framework   | FastAPI                 |
| Database    | MongoDB Atlas (pymongo) |
| Auth        | JWT (python-jose)       |
| Config      | python-dotenv           |
| Server      | Uvicorn (ASGI)          |

---

## 📁 Project Structure

```
Inventory_api/
├── main.py            # API routes (POST, GET by ID, GET by name)
├── models.py          # Pydantic request/response models
├── database.py        # MongoDB Atlas connection
├── jwt_handler.py     # JWT token generation and verification
├── .env               # Environment variables (keep this secret!)
├── requirements.txt   # Python dependencies
└── pyproject.toml     # Project metadata
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Inventory_api
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (or update the existing one):

```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?appName=Cluster0
DB_NAME=inventory_db
SECRET_KEY=your_super_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ **Never commit your `.env` file to version control.** Add it to `.gitignore`.

---

## 🚀 Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

---

## 📖 API Reference

### Base URL
```
http://127.0.0.1:8000
```

---

### ➕ Create an Item

**`POST /items`**

Creates a new inventory item. Item names must be **unique** — attempting to create a duplicate name returns a `409 Conflict` error.

**Request Body:**
```json
{
  "id": "string",
  "name": "string",
  "quantity": 0,
  "category": "string"
}
```

**Success Response `201 Created`:**
```json
{
  "message": "Item created successfully",
  "id": "664f1a2b3c4d5e6f7a8b9c0d",
  "item": {
    "id": "664f1a2b3c4d5e6f7a8b9c0d",
    "name": "Laptop",
    "quantity": 10,
    "category": "Electronics"
  }
}
```

**Duplicate ID Response `409 Conflict`:**
```json
{
  "detail": "An item with id 'item-001' already exists"
}
```

**Duplicate Name Response `409 Conflict`:**
```json
{
  "detail": "An item with name 'Laptop' already exists (id: item-001)"
}
```

---

### 🔍 Get Item by ID

**`GET /items/id/{item_id}`**

Fetch a single item using the ID you assigned when creating it.

**Example:**
```
GET /items/id/item-001
```

**Success Response `200 OK`:**
```json
{
  "id": "item-001",
  "name": "Laptop",
  "quantity": 10,
  "category": "Electronics"
}
```

**Error Response:**
- `404 Not Found` — No item with that ID exists

---

### 🔍 Get Item by Name

**`GET /items/name/{name}`**

Fetch a single item using its exact name.

**Example:**
```
GET /items/name/Laptop
```

**Success Response `200 OK`:**
```json
{
  "id": "item-001",
  "name": "Laptop",
  "quantity": 10,
  "category": "Electronics"
}
```

**Error Response:**
- `404 Not Found` — No item with that name exists

---

## 🔐 Authentication (JWT)

The project includes a JWT handler (`jwt_handler.py`) for protecting routes.

### How it works:
1. **Generate a token** by calling `generate_token({"sub": "user_id"})`.
2. **Protect a route** by adding `Depends(require_token)` to the endpoint.
3. Clients must pass the token in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

Tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30 minutes).

---

## 🧪 Interactive API Docs

FastAPI provides built-in interactive documentation:

| UI        | URL                                  |
|-----------|--------------------------------------|
| Swagger   | http://127.0.0.1:8000/docs           |
| ReDoc     | http://127.0.0.1:8000/redoc          |

---

## 🌱 Environment Variables Reference

| Variable                   | Description                         | Default |
|---------------------------|-------------------------------------|---------|
| `MONGO_URI`               | MongoDB Atlas connection string     | —       |
| `DB_NAME`                 | Database name                       | —       |
| `SECRET_KEY`              | Secret key for JWT signing          | —       |
| `ALGORITHM`               | JWT signing algorithm               | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time in minutes    | `30`    |

---

## 📝 Notes

- Item **names are unique** — enforced at the application layer.
- Item **IDs are provided by the user** — you choose the ID when creating an item (e.g. `"item-001"`, `"laptop-1"`).
- Both `id` and `name` must be unique; a `409 Conflict` is returned if either already exists.
- The user-provided `id` is stored as MongoDB's `_id` field internally.
- The database connection uses `tlsAllowInvalidCertificates=True` for local development compatibility — tighten this for production.
