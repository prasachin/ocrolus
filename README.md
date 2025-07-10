# ocrolus Backend Assignment

### This is the Backend basic architecture diagram.

![structurizr-104370-Container-001(1)](https://github.com/user-attachments/assets/7ed471f8-abea-4b16-b166-2febf2db4883)

## Tech Stack

- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: ORM for database operations
- **JWT**: JSON Web Tokens for authentication
- **Bcrypt**: Password hashing
- **In-memory storage**: Recently viewed articles tracking

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses JWT Bearer token authentication. After logging in, include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

---

## Authentication Endpoints

### 1. Register User

**POST** `/auth/register`

Register a new user account.

**Request Body:**

```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response (201 Created):**

```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2025-07-10T10:00:00Z",
  "updated_at": null
}
```

**Error Responses:**

- `400 Bad Request`: Username or email already exists

---

### 2. Login User

**POST** `/auth/login`

Authenticate user and receive JWT token.

**Request Body (Form Data):**
```
username: string
password: string
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials

---

### 3. Get Current User Profile

**GET** `/auth/me`

Get the current authenticated user's profile.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2025-07-10T10:00:00Z",
  "updated_at": null
}
```

---

