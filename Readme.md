# Bookly - Book Management System

## Overview

Bookly is a robust Book Management System built with FastAPI, providing a RESTful API service for managing books, reviews, and user interactions. The system implements secure authentication, role-based access control, and asynchronous database operations.

## Features

### Core Features
- **Book Management**: CRUD operations for books with detailed metadata
- **User Authentication**: JWT-based secure authentication system
- **Review System**: Allow users to review and rate books
- **Tag Management**: Organize books with customizable tags
- **Role-Based Access**: Admin and user role differentiation
- **Email Verification**: Secure user registration with email verification

### Technical Features
- **Async Database**: PostgreSQL with SQLModel for async operations
- **Mail Integration**: SMTP email service for notifications
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Error Handling**: Comprehensive error management system

## Project Structure

```
bookly/
├── src/
│   ├── auth/
│   │   ├── dependencies.py    # Auth middleware and dependencies
│   │   ├── routes.py         # Authentication endpoints
│   │   ├── services.py       # Auth business logic
│   │   └── utils.py          # JWT and password utilities
│   ├── books/
│   │   ├── routes.py         # Book management endpoints
│   │   └── services.py       # Book-related operations
│   ├── reviews/
│   │   ├── routes.py         # Review management endpoints
│   │   └── services.py       # Review operations
│   ├── tags/
│   │   ├── routes.py         # Tag management endpoints
│   │   └── services.py       # Tag operations
│   ├── db/
│   │   ├── models.py         # SQLModel database models
│   │   └── main.py          # Database connection management
│   └── config.py            # Application configuration
├── tests/                   # Unit and integration tests
└── migrations/                # Database migrations
```

## API Endpoints

### Authentication
- **POST /api/v1/auth/send-mail** : Send verification email
- **POST /api/v1/auth/signup** : Register new user
- **POST /api/v1/auth/login** : Login user
- **GET /api/v1/auth/verify/{token}** : Verify user email
- **GET /api/v1/auth/refresh-token** : Get new access token
- **GET /api/v1/auth/me** : Get current user details
- **POST /api/v1/auth/password-reset** : Request password reset
- **POST /api/v1/auth/password-reset-confirm/{token}** : Reset password with token
  

### Books
- **GET /api/v1/books/** : List all books
- **POST /api/v1/books/** : Create new book
- **GET /api/v1/books/user/{user_id}** : Get books by user ID
- **GET /api/v1/books/{book_id}** : Get book details by ID
- **PATCH /api/v1/books/{book_id}** : Update book details
- **DELETE /api/v1/books/{book_id}** : Delete a book

### Reviews
- **POST /api/v1/reviews/book/{book_id}**: Add Review
- **GET /api/v1/reviews**: Get all reviews
- **GET /api/v1/reviews/{review_id}**: Get review by Id
- **DELETE /api/v1/reviews/{review_id}**: Delete review

### Tags
- **GET /api/v1/tags**: List all tags
- **POST /api/v1/tags**: Create tag
- **GET /api/v1/tags/{tag_id}** : Get Tag By Id
- **PATCH /api/v1/tags/{tag_id}** : Update Tags
- **DELETE /api/v1/tags/{tag_id}** : Delete Tags
- **POST /api/v1/tags/book/{book_id}**: Add tags to book

## Setup and Installation

### Prerequisites
- Python 3.11+
- PostgreSQL


### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv env
   .\env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/bookly
   JWT_SECRET=your-secret-key
   JWT_ALGORITHM=HS256
   MAIL_USERNAME=your-email
   MAIL_PASSWORD=your-password
   MAIL_FROM=noreply@bookly.com
   MAIL_PORT=587
   MAIL_SERVER=smtp.gmail.com
   ```

5. Run migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the server:
   ```bash
   fastapi dev src/ #This is for development mode

   fastapi run src/ #This is for production mode
   ```

7. View Documentation:
   ```bash
   
   localhost:8000/docs #Swagger UI Documentation

   localhost:8000/redoc #Redoc UI Documentation
   ```

## Development

### Running Tests
```bash
pytest tests/
```

### Creating Migrations
```bash
alembic revision --autogenerate -m "migration message"
alembic upgrade head
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document functions and classes

## Error Handling

The system implements custom error classes:
- `InvalidToken`
- `AccountNotVerified`
- `InsufficientPermission`
- `BookNotFound`
- `TagNotFound`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.