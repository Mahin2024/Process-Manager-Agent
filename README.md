# Process Manager Agent

A full-stack project that collects system and process information from your computer and displays it on a web dashboard.

## Project Structure

PROCESS_MANAGER_AGENT/
├── agent/ # Agent script to collect system/process info
│ └── agent.py # Runs locally using psutil
├── base/ # Django project configuration
│ ├── asgi.py # ASGI entry point (async support)
│ ├── settings.py # Global project settings
│ ├── urls.py # Root URL routing
│ └── wsgi.py # WSGI entry point (deployment)
├── process/ # Django app for process management
│ ├── migrations/ # Database migrations
│ ├── admin.py # Django admin configuration
│ ├── apps.py # App setup
│ ├── authentication.py # Custom authentication logic
│ ├── models.py # Database models
│ ├── serializers.py # Django REST Framework serializers
│ ├── tests.py # Unit tests
│ ├── urls.py # App-specific routes
│ └── views.py # Views & API endpoints
├── templates/ # HTML templates
│ └── index.html # Main dashboard
├── db.sqlite3 # SQLite DB (for development)
├── manage.py # Django management script
├── requirements.txt # Dependencies (pip-based)
├── Pipfile / Pipfile.lock # Pipenv dependency management
└── run_app.bat # Startup script (Windows)

## Setup Instructions

1. Clone the project or download it to your machine.
2. Make sure Python 3.10+ is installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
Running the Project
Double-click run_app.bat 

The script will:

Start the Django backend server.

Start the agent that collects system info and processes.

Open the frontend dashboard in your default browser.

Wait a few seconds; the dashboard will display your system and process information.

How It Works
Agent (agent.py): Uses psutil to gather real system/process info and sends it to the backend APIs:

http://127.0.0.1:8000/api/system-info/

http://127.0.0.1:8000/api/processes/bulk/

Django Backend: Receives and stores the data.