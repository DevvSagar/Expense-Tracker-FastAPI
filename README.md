# Expense Tracker API

A RESTful Expense Tracker API built with FastAPI, featuring JWT authentication, per-user data ownership, and category-based expense filtering/summaries.

## Features

- **User Authentication** — Register and log in with hashed passwords and JWT-based access tokens
- **Protected Routes** — All expense endpoints require a valid bearer token
- **Per-User Ownership** — Each user can only view, edit, or delete their own expenses
- **Full CRUD** — Create, read, update, and delete expenses
- **Category Filtering** — Filter expenses by category
- **Totals & Summaries** — Get total spend and category-wise summaries
- **Database Migrations** — Schema versioned with Alembic
- **Containerized** — Runs with Docker and PostgreSQL via `docker-compose`

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Validation:** Pydantic
- **Auth:** JWT (JSON Web Tokens), password hashing
- **Containerization:** Docker / Docker Compose

## Project Structure

```
.
├── models/          # SQLAlchemy database models
├── schemas/         # Pydantic request/response schemas
├── routers/         # API route definitions
├── security.py       # Password hashing & JWT logic
├── dependencies.py   # Auth dependency (current-user extraction)
├── database.py        # DB session/engine setup
├── main.py            # FastAPI app entrypoint
├── alembic/          # Migration scripts
└── docker-compose.yml
```

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.10+

### Setup

```bash
# Clone the repo
git clone https://github.com/DevvSagar/expense-tracker-api.git
cd expense-tracker-api

# Start the Postgres container
docker-compose up -d

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs (Swagger UI) at `http://localhost:8000/docs`.

## API Endpoints

| Method | Endpoint                    | Description                       | Auth Required |
|--------|-------------------------------|-------------------------------------|----------------|
| POST   | `/auth/register`             | Register a new user                 | No             |
| POST   | `/auth/login`                | Log in and receive a JWT            | No             |
| GET    | `/expenses`                  | List the current user's expenses    | Yes            |
| GET    | `/expenses/{id}`             | Get a single expense                | Yes            |
| GET    | `/expenses/category/{name}`  | Filter expenses by category         | Yes            |
| GET    | `/expenses/total`            | Get total spend                     | Yes            |
| GET    | `/expenses/summary`          | Get category-wise summary           | Yes            |
| POST   | `/expenses`                  | Create a new expense                | Yes            |
| PUT    | `/expenses/{id}`             | Update an expense                   | Yes            |
| DELETE | `/expenses/{id}`             | Delete an expense                   | Yes            |

## Authentication

Include the JWT in the `Authorization` header for protected routes:

```
Authorization: Bearer <your_token>
```

## License

MIT
