# Blog Management API

A RESTful API built with FastAPI, SQLAlchemy, SQLite, and JWT authentication for managing blog posts and user accounts.

## Features

- **JWT Authentication**: Secure token-based user authentication (OAuth2 with Password Bearer flow).
- **Password Hashing**: Secure password storage using `bcrypt`.
- **CRUD Operations**: Full Create, Read, Update, and Delete endpoints for blog posts.
- **Ownership Enforcement**: Users can only update or delete their own blog posts.
- **Pydantic Validation**: Request and response schema validation using Pydantic.
- **Auto-generated Documentation**: Interactive OpenAPI documentation accessible at `/docs` or `/redoc`.
- **Pytest Suite**: Complete test coverage for authentication, authorization, and CRUD endpoints.

## Setup Instructions

1. **Create and Activate a Virtual Environment**
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Configure Environment Variables**
   Copy `.env.example` to `.env` (or set `SECRET_KEY` in your environment):
   ```bash
   cp .env.example .env
   ```
   Generate a secret key with:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Set `SECRET_KEY` in `.env` or set environment variable:
   ```bash
   # Windows PowerShell
   $env:SECRET_KEY="your_secret_key_here"
   # Linux/macOS
   export SECRET_KEY="your_secret_key_here"
   ```

4. **Run the Server**
   ```bash
   uvicorn blog.main:app --reload
   ```
   Access the interactive API docs at `http://127.0.0.1:8000/docs`.

## API Endpoints

| Method | Path | Auth Required | Description |
| --- | --- | --- | --- |
| `POST` | `/user/` | No | Register a new user account (returns 409 if email exists). |
| `GET` | `/user/{id}` | No | Get user details by user ID. |
| `POST` | `/login` | No | Authenticate user and receive JWT access token. |
| `GET` | `/blog/` | Yes | Retrieve all blog posts. |
| `POST` | `/blog/` | Yes | Create a new blog post associated with the current user. |
| `GET` | `/blog/{id}` | Yes | Retrieve a specific blog post by ID. |
| `PUT` | `/blog/{id}` | Yes | Update a blog post (owner only). |
| `DELETE` | `/blog/{id}` | Yes | Delete a blog post (owner only). |

## Running Tests

Run `pytest` to execute all API test cases:
```bash
pytest
```

## Project Structure

```
FastApi/
├── blog/
│   ├── __init__.py
│   ├── database.py
│   ├── hashing.py
│   ├── main.py
│   ├── models.py
│   ├── oauth2.py
│   ├── schemas.py
│   └── token.py
│   └── routers/
│       ├── __init__.py
│       ├── authentication.py
│       ├── blog.py
│       └── user.py
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── requirements-dev.txt
```
