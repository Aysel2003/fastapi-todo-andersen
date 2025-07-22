# fastapi-todo-andersen

 A Dockerized FastAPI ToDo REST API with user authentication, PostgreSQL integration, and pagination.
 
 ## Project documentation
 
 This is a simple RESTful API application for a ToDo list on the FastAPI framework. Every part of this project is code which displays how to do the following:
 1. Create user and task models with the given followings on the FastApi framework
 2. Implement CRUD operations and API endpoints using FastApi
 3. Add user authentication and authorization using JWT
 4. Implement pagination for the task list (I did this one for the first two get operations)
 5. Connect to PostgreSQL as a database for storing data
 6. Dockerize the application

## Installation instructions

1. Clone the repository:
   1. git clone https://github.com/Aysel2003/fastapi-todo-andersen.git
   2. cd fastapi-todo-andersen
2. Build and run the application using Docker Compose: docker compose up --build

## API documentation 

1. FastAPI gives us built-in docs:
Swagger UI (interactive user interface): http://localhost:8000/docs - This one helps users use and work with endpoints manually.
ReDoc: http://localhost:8000/redoc - This provides with clean amd more structured documentation for end-users. 
3. In this UI, there will be API endpoints overview:
   | Method | Endpoint                   | Description                |
   |--------|----------------------------|----------------------------|
   | GET    | '/tasks'                   | Get all tasks              |
   | GET    | '/tasks/user/{user_id}'    | Get all user's tasks       |
   | GET    | '/tasks/{task_id}'         | Get a specific task        |
   | POST   | '/tasks'                   | Create a new task          |
   | PUT    | '/tasks/{task_id}'         | Update a task (by owner)   |
   | DELETE | '/tasks/{task_id}'         | Delete a task (by owner)   |
   | POST   | '/tasks/{task_id}/complete'| Mark a task as completed   |
   | GET    | '/tasks-by-status'         | Filter tasks by status     |
   
## Dockerization

The application has been **Dockerized** for easy deployment and environment consistency. A 'Dockerfile' is included to containerize the FastAPI application, and a 'compose.yml' file is provided to manage and run the application with a single command: docker compose up --build

## Testing

Unit tests have been created for each API endpoint using FastAPI's 'TestClient'. All tests are designed to validate successful outcomes and currently **pass successfully (8 passed)**.
To run the unit tests inside a Docker container, use the following command: docker compose run web pytest

### Test Setup Requirements

- Certain tests (e.g., get (according to user_id, or task_id) update and delete) operate on pre-existing task and user IDs.
- Therefore, you must manually create required tasks and users in advance within the framework to ensure those IDs exist before running the tests.

### Authentication Notes

- The application requires user authentication for protected endpoints.
- Before running the tests, you need to **obtain a valid access token** by logging in.
- Insert this token into the test file manually to avoid `401 Unauthorized` errors.

### Owner-Restricted Endpoints

- Endpoints like `DELETE /tasks/{id}` and `PUT /tasks/{id}` are restricted to the **task owner**.
- To ensure valid behavior, a test task is created under the current user (simulated with the token), so the test has permission to modify or delete it.

### Project SetUp Improvements

For the purpose of improving cross-platform compatibility and security, the following changes were made:
- Docker Compose now runs both the app and the database
The docker-compose.yml file was updated to include a db service using PostgreSQL. This ensures the entire infrastructure run together inside containers.
- Removed hardcoded credentials from the connection URL
Database credentials (username, password, database name) are no longer written directly in the code. Instead, they are stored in a .env file and loaded via environment variables.
- Replaced platform-specific hostname (host.docker.internal) with db
The hostname used for database connection is now db, which refers to the database service in Docker Compose. This makes the setup compatible across Linux, Windows, and macOS.

   
  

