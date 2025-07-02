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
   git bash
   git clone https://github.com/Aysel2003/fastapi-todo-andersen.git
   cd fastapi-todo-andersen
2. Create and activate a virtual environment:
   python -m venv venv
   source venv/Scripts/activate
3. Install dependencies:
   pip install -r requirements.txt
## API documentation 
1. FastAPI gives us built-in docs:
   Swagger UI (interactive user interface): http://localhost:8000/docs
   This one helps users use and work with endpoints manually.
2. In this UI, there will be API endpoints overview:
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

   
  

