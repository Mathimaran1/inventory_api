# Inventory Management API

A simple REST API built using **FastAPI** and **MongoDB Atlas** to manage inventory items. It allows users to:

* Add new items
* Get items by ID
* Get items by name
* Use JWT authentication for protected routes

## Tech Used

* FastAPI
* MongoDB Atlas
* JWT Authentication
* Uvicorn

## Project Structure

```bash
Inventory_api/
│
├── main.py
├── models.py
├── database.py
├── jwt_handler.py
├── .env
├── requirements.txt
└── pyproject.toml
```

## Setup

### 1. Clone the project

```bash
git clone <repo-url>
cd Inventory_api
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file:

```env
MONGO_URI=your_mongodb_uri
DB_NAME=inventory_db
```

## Run the Server

```bash
uvicorn main:app --reload
```

Server runs at:

```bash
http://127.0.0.1:8000
```

## API Endpoints

### Create Item

**POST** `/items`

Example request:

```json
{
  "id": "item-001",
  "name": "Laptop",
  "quantity": 10,
  "category": "Electronics"
}
```

### Get Item by ID

**GET** `/items/id/{item_id}`

Example:

```bash
/items/id/item-001
```

### Get Item by Name

**GET** `/items/name/{name}`

Example:

```bash
/items/name/Laptop
```

## API Documentation

FastAPI provides built-in docs:

* Swagger UI → `http://127.0.0.1:8000/docs`

## Notes

* Item IDs and names must be unique
* Duplicate entries return `409 Conflict`
* MongoDB stores the provided `id` as `_id`

