# ocrolus Backend Assignment

### This is the Backend basic architecture diagram.

#### **_Note: This is a simplified version of the architecture diagram.There is no any admin panel or frontend in this project._**

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

## Article Management Endpoints

### 4. Create Article

**POST** `/articles/`

Create a new article. Only authenticated users can create articles.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Request Body:**

```json
{
  "title": "My First Article",
  "content": "This is the content of my article..."
}
```

**Response (201 Created):**

```json
{
  "id": 1,
  "title": "My First Article",
  "content": "This is the content of my article...",
  "author_id": 1,
  "created_at": "2025-07-10T10:00:00Z",
  "updated_at": null,
  "author": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

---

### 5. Get Articles (Paginated)

**GET** `/articles/`

Retrieve a paginated list of articles ordered by creation date (newest first).

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Query Parameters:**

- `page` (optional): Page number (default: 1, min: 1)
- `page_size` (optional): Items per page (default: 10, min: 1, max: 100)

**Example Request:**

```
GET /articles/?page=1&page_size=5
```

**Response (200 OK):**

```json
{
  "articles": [
    {
      "id": 3,
      "title": "Latest Article",
      "content": "Content here...",
      "author_id": 1,
      "created_at": "2025-07-10T12:00:00Z",
      "updated_at": null,
      "author": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
      }
    },
    {
      "id": 2,
      "title": "Second Article",
      "content": "More content...",
      "author_id": 2,
      "created_at": "2025-07-10T11:00:00Z",
      "updated_at": null,
      "author": {
        "id": 2,
        "username": "jane_doe",
        "email": "jane@example.com"
      }
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 5,
  "total_pages": 3
}
```

---

### 6. Get Article by ID

**GET** `/articles/{article_id}`

Get a specific article by its ID. This endpoint also tracks the article as recently viewed.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**

- `article_id`: Integer ID of the article

**Response (200 OK):**

```json
{
  "id": 1,
  "title": "My First Article",
  "content": "This is the content of my article...",
  "author_id": 1,
  "created_at": "2025-07-10T10:00:00Z",
  "updated_at": null,
  "author": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

**Error Responses:**

- `404 Not Found`: Article not found

---

### 7. Update Article

**PUT** `/articles/{article_id}`

Update an existing article. Only the author can update their own articles.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**

- `article_id`: Integer ID of the article

**Request Body:**

```json
{
  "title": "Updated Article Title",
  "content": "Updated content here..."
}
```

**Note**: Both `title` and `content` are optional. You can update just one field.

**Response (200 OK):**

```json
{
  "id": 1,
  "title": "Updated Article Title",
  "content": "Updated content here...",
  "author_id": 1,
  "created_at": "2025-07-10T10:00:00Z",
  "updated_at": "2025-07-10T14:00:00Z",
  "author": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

**Error Responses:**

- `404 Not Found`: Article not found
- `403 Forbidden`: Not the author of the article

---

### 8. Delete Article

**DELETE** `/articles/{article_id}`

Delete an article. Only the author can delete their own articles.

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**

- `article_id`: Integer ID of the article

**Response (204 No Content):**
No response body.

**Error Responses:**

- `404 Not Found`: Article not found
- `403 Forbidden`: Not the author of the article

---

### 9. Get Recently Viewed Articles

**GET** `/articles/recently-viewed/me`

Get the current user's recently viewed articles (up to 10 most recent).

**Headers:**

```
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**

```json
[
  {
    "id": 5,
    "title": "Recently Viewed Article",
    "author_id": 2,
    "viewed_at": "2025-07-10T13:30:00Z",
    "author": {
      "id": 2,
      "username": "jane_doe",
      "email": "jane@example.com",
      "is_active": true,
      "created_at": "2025-07-10T09:00:00Z",
      "updated_at": null
    }
  },
  {
    "id": 3,
    "title": "Another Article",
    "author_id": 1,
    "viewed_at": "2025-07-10T13:00:00Z",
    "author": {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "is_active": true,
      "created_at": "2025-07-10T08:00:00Z",
      "updated_at": null
    }
  }
]
```

---

## Default Endpoints

### 10. Health Check

**GET** `/health`

Check API health status.

**Response (200 OK):**

```json
{
  "status": "healthy",
  "timestamp": "2025-07-10T10:00:00Z"
}
```

### 11. Root Endpoint

**GET** `/`

API root endpoint.

**Response (200 OK):**

```json
{
  "message": "Welcome to Article Management API",
  "version": "1.0.0"
}
```

---

## Technical Implementation Details

### Authentication Flow

1. **Registration**: User provides username, email, and password
2. **Password Hashing**: Bcrypt is used to hash passwords before storage
3. **Login**: User authenticates with username/password
4. **JWT Token**: Server generates JWT token with user information
5. **Protected Routes**: All article endpoints require valid JWT token

### Recently Viewed Articles

- **Storage**: In-memory using Python collections (deque)
- **Capacity**: Maximum 10 articles per user
- **Behavior**: Most recently viewed articles appear first
- **Deduplication**: Viewing the same article again moves it to the top

### Pagination

- **Default**: 10 articles per page
- **Limits**: 1-100 articles per page
- **Ordering**: Articles ordered by creation date (newest first)
- **Metadata**: Response includes total count, pages, and current page info

### Error Handling

The API uses standard HTTP status codes:

- `200 OK`: Successful GET requests
- `201 Created`: Successful POST requests
- `204 No Content`: Successful DELETE requests
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or invalid
- `403 Forbidden`: Access denied (e.g., not article author)
- `404 Not Found`: Resource not found

### Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Authorization**: Users can only modify their own articles
- **Input Validation**: Pydantic schemas for request validation

---

## Unit Tests

Unit tests are provided to ensure the functionality of the API endpoints. The tests cover:

- User registration and login
- Article creation, retrieval, updating, and deletion
- Recently viewed articles tracking
- Pagination and ordering of articles
- Error handling scenarios
- Authentication and authorization checks
- Health check endpoint
- Root endpoint response
- all the 17 checks are there.

## schemas Changelog Management

The `schemas` Changelog Management system is implemented using ambelic. It allows for versioning and tracking changes to the API schemas over time. Each schema change is documented with a version number, description, and date of change.  
This ensures that the API remains backward compatible and allows for easy migration of clients to newer versions.

## Running the Application

To run the application, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone

   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd ocrolus
   ```
3. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```
4. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
5. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
6. **Set Up the Environment Variables**:
   Create a `.env` file in the root directory and add the following variables:

   ```bash
   # .env
   DATABASE_URL=mysql+mysqlconnector://root:Ra62052Sa%40@localhost/CMS_db
   SECRET_KEY=ocrolus_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

   **_Note: Make sure to replace the `DATABASE_URL` with your actual database connection string._**

7. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload
   ```
8. **Access the API**:
   Open your browser and go to `http://localhost:8000/docs` to view the
   interactive API documentation (Swagger UI).

## Testing the Application

To run the tests, ensure you have `pytest` installed. You can run the all the tests using the following command:

```bash
pytest
```

## Running schemas Changelog Management

To run the schemas Changelog Management, you can use the following useful commands:

- `alembic init` Creates folders like versions/, and a config file alembic.ini.
- `alembic revision -m "<message>"` Generates a new empty migration script with the given message.
- `alembic revision --autogenerate -m "<message>"` Generates a new migration script with the changes detected in the models.
- `alembic upgrade <target>` Applies the migration to the target version.
- `alembic downgrade <target>` Reverts the migration to the target version.
- `alembic history` Shows the history of migrations applied to the database.
- `alembic current` Shows the current version of the database schema.
