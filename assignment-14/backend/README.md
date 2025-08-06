# Todo List API

## Product Requirements Document (PRD)

### Overview
This project aims to develop an API for a Todo List application with multiple features to help users organize and manage their tasks efficiently.

### Requirements
1. **Multiple Lists**: Support for creating and managing multiple task lists for better organization.
2. **List Management**:
   - View all lists and their associated tasks
   - Create new lists
   - Update existing lists
   - Delete lists
3. **Task Management**:
   - Add tasks to a specific list
   - Update task details
   - Delete tasks
   - Mark tasks as completed
4. **Task Deadline Features**:
   - Set deadlines for tasks
   - View tasks due in the current week
   - Sort tasks based on deadlines

### Technical Implementation Plan

#### Goals
Develop a RESTful API using FastAPI that meets all the requirements specified above, with a clean and maintainable codebase.

#### Technology Stack
- **Framework**: FastAPI
- **Language**: Python
- **Database**: JSON file-based storage (initial implementation)
- **Environment**: Virtual Environment (venv)

#### Directory Structure
```
assignment-8/
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── list_routes.py
│   │   │   └── task_routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── data.json
│   ├── models/
│   │   ├── __init__.py
│   │   ├── list_model.py
│   │   └── task_model.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── list_schema.py
│   │   └── task_schema.py
│   └── services/
│       ├── __init__.py
│       ├── list_service.py
│       └── task_service.py
└── tests/
    ├── __init__.py
    ├── test_list_api.py
    └── test_task_api.py
```

#### Code Structure Pattern
- **Repository Pattern**: Separate data access logic
- **Service Layer**: Business logic implementation
- **API Routes**: HTTP endpoints for client interaction
- **Pydantic Models**: Data validation and serialization

#### Testing Strategy
- Unit tests for service and repository functions
- Integration tests for API endpoints using TestClient
- Test coverage for all main functionalities

#### Implementation Phases

**Phase 1: Project Setup**
- [x] Set up project structure
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Set up basic FastAPI application

**Phase 2: Data Models and Schemas**
- [ ] Define data models for lists and tasks
- [ ] Create Pydantic schemas for request/response validation
- [ ] Implement JSON database storage

**Phase 3: Core Functionality - Lists**
- [ ] Implement list creation
- [ ] Implement list retrieval (single and all)
- [ ] Implement list update
- [ ] Implement list deletion

**Phase 4: Core Functionality - Tasks**
- [ ] Implement task creation within lists
- [ ] Implement task retrieval
- [ ] Implement task update
- [ ] Implement task deletion
- [ ] Implement task completion toggle

**Phase 5: Advanced Task Features**
- [ ] Implement deadline setting for tasks
- [ ] Implement retrieval of tasks due this week
- [ ] Implement task ordering based on deadline

**Phase 6: Testing and Documentation**
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Create API documentation
- [ ] Final review and bug fixes

### API Endpoints

#### Lists
- `GET /api/lists` - Get all lists
- `GET /api/lists/{list_id}` - Get a specific list with its tasks
- `POST /api/lists` - Create a new list
- `PUT /api/lists/{list_id}` - Update a list
- `DELETE /api/lists/{list_id}` - Delete a list

#### Tasks
- `GET /api/lists/{list_id}/tasks` - Get all tasks in a list
- `GET /api/lists/{list_id}/tasks/{task_id}` - Get a specific task
- `POST /api/lists/{list_id}/tasks` - Add a task to a list
- `PUT /api/lists/{list_id}/tasks/{task_id}` - Update a task
- `DELETE /api/lists/{list_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/lists/{list_id}/tasks/{task_id}/complete` - Mark a task as completed/uncompleted

#### Special Task Endpoints
- `GET /api/tasks/due-this-week` - Get tasks due this week
- `GET /api/lists/{list_id}/tasks/ordered` - Get tasks ordered by deadline

## Getting Started

(Implementation instructions will be added as development progresses)
