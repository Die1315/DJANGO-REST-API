# Project Management API

A Django REST API for managing projects and tasks with user authentication and team collaboration features.

## Features

- **User Management**: Custom user model with email authentication
- **Project Management**: Create, update, and manage projects
- **Task Management**: Create tasks with status tracking (To Do, In Progress, Done)
- **Team Collaboration**: Assign users to teams
- **REST API**: Full RESTful API with token authentication
- **Database**: PostgreSQL database support

## Prerequisites

Before running this application, make sure you have the following installed:

- **Python 3.8+**
- **PostgreSQL** (for production) or **SQLite** (for development)
- **pip** (Python package installer)
- **Git** (for cloning the repository)

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd project_managements
```

### Step 2: Create a Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

The project includes a `requirements.txt` file with all necessary dependencies:

```txt
asgiref==3.9.1
colorama==0.4.6
Django==5.2.4
djangorestframework==3.16.0
flake8==7.3.0
iniconfig==2.1.0
isort==6.0.1
mccabe==0.7.0
packaging==25.0
pluggy==1.6.0
psycopg==3.2.9
psycopg2==2.9.10
pycodestyle==2.14.0
pyflakes==3.4.0
Pygments==2.19.2
pytest==8.4.1
pytest-django==4.11.1
python-decouple==3.8
sqlparse==0.5.3
tzdata==2025.2
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
DB_NAME=project_management_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

**For Development (SQLite):**
If you want to use SQLite for development, modify the `DATABASES` setting in `project_managements/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Step 5: Database Setup

```bash
# Run database migrations
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user with email, first name, and last name.

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication
- `POST /api/token/` - Get authentication token
- `POST /api/token/refresh/` - Refresh authentication token

### Users
- `GET /api/users/` - List all users
- `POST /api/users/` - Create a new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Teams
- `GET /api/teams/` - List all teams
- `POST /api/teams/` - Create a new team
- `GET /api/teams/{id}/` - Get team details
- `PUT /api/teams/{id}/` - Update team
- `DELETE /api/teams/{id}/` - Delete team

### Projects
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create a new project
- `GET /api/projects/{id}/` - Get project details
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project

### Tasks
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task

## API Usage Examples

### Authentication
```bash
# Get authentication token
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword"}'
```

### Create a Project
```bash
# Create a new project
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "description": "Project description",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31"
  }'
```

### Create a Task
```bash
# Create a new task
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Token your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "project": 1,
    "title": "Complete API Documentation",
    "description": "Write comprehensive API documentation",
    "status": "todo"
  }'
```

## Testing

Run the test suite:

```bash
# Run all tests
python manage.py test

# Run tests with pytest
pytest

# Run tests with coverage
pytest --cov=.
```

## Project Structure

```
project_managements/
├── authorisation/          # Authorization app
├── core/                   # Core functionality (projects, tasks)
├── users/                  # User management and teams
├── project_managements/    # Main project settings
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md             # This file
```

## Development

### Adding New Features
1. Create a new Django app: `python manage.py startapp app_name`
2. Add the app to `INSTALLED_APPS` in `settings.py`
3. Create models, serializers, and views
4. Add URL patterns
5. Create and run migrations

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write tests for new features

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env` file
   - Verify database exists

2. **Migration Errors**
   - Delete migration files and recreate them
   - Reset database if needed: `python manage.py flush`

3. **Import Errors**
   - Ensure virtual environment is activated
   - Install missing dependencies: `pip install -r requirements.txt`

4. **Port Already in Use**
   - Use a different port: `python manage.py runserver 8001`
   - Kill the process using the port

## Production Deployment

For production deployment, consider:

1. **Environment Variables**: Set `DEBUG=False` and use a strong `SECRET_KEY`
2. **Database**: Use a production PostgreSQL database
3. **Static Files**: Configure static file serving
4. **Security**: Use HTTPS, configure CORS, and set up proper authentication
5. **WSGI Server**: Use Gunicorn or uWSGI instead of the development server

