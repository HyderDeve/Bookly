# Book Management System 'Bookly'

## Overview

Welcome to Bookly, a comprehensive Book Management System designed to manage and review books effectively. Built with FastAPI, this RESTful API service provides a robust framework for handling book-related operations.

## Features

- **Book Management**: Add, update, delete, and retrieve book details with ease.
- **User Authentication**: Secure user registration and login functionalities.
- **Database Integration**: Asynchronous database operations with SQLModel and PostgreSQL.
- **Scalable Architecture**: Modular code structure to support future expansions.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd bookly
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

- Start the server:
  ```bash
  uvicorn main:app --reload
  ```
- Access the API documentation at `http://localhost:8000/docs`.

## API Endpoints

- **GET /api/v1/books**: Retrieve all books.
- **POST /api/v1/books**: Add a new book.
- **PATCH /api/v1/books/{id}**: Update book details.
- **DELETE /api/v1/books/{id}**: Remove a book.

## Configuration

- The application settings are managed via environment variables in a `.env` file.
- Ensure the database URL is correctly set in the configuration.

## Database

- Utilizes Alembic for database migrations.
- Supports asynchronous operations for enhanced performance.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for improvements or bug fixes.

## License

Bookly is open-source software licensed under the MIT License.
