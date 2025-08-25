# Process Manager Agent

A Process-Manager-Agent-with-Django-Backend-Project
A real-time process monitoring agent with a Django backend and Python agent. Displays system processes in a live, tree-structured UI with CPU & memory usage. Built for professional system monitoring and task management.

📄 README.md

🖥️ Process Monitoring Agent (Django + Python)
A powerful and simple process monitoring web application built with Django and Python. This project allows you to track and display real-time process trees from multiple machines using a background agent and a web-based frontend.


## 📌 Features
- Real-time system and process monitoring  
- CPU & memory usage for each process  
- Host-wise filtering and search  
- REST API powered by Django + DRF  
- Lightweight agent using psutil  
- Easy startup with `run_app.bat`  
- Responsive dashboard built with HTML/JS  

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

Django Backend: Receives and stores the data.



---

🧠 Architecture Overview
[Agent Script] ---> [Django Backend] ---> [Frontend Dashboard]
↑
(Runs on Host)


- **Agent (`agent.py`)**: Collects live process/system info using `psutil` and pushes to backend APIs  
- **Django Backend**: Provides API endpoints and stores data in SQLite  
- **Frontend Dashboard**: Fetches data from backend and renders process list in browser  

---

📂 Project Structure

PROCESS_MANAGER_AGENT/
├── agent/
│ └── agent.py # Python script that collects system/process info
│
├── base/ # Django project configuration
│ ├── init.py
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── process/ # Django app for process management
│ ├── init.py
│ ├── admin.py
│ ├── apps.py
│ ├── authentication.py
│ ├── models.py
│ ├── serializers.py
│ ├── tests.py
│ ├── urls.py
│ └── views.py
│
├── templates/
│ └── index.html # Dashboard frontend
│
├── db.sqlite3 # SQLite DB (development only)
├── manage.py # Django management script
├── requirements.txt # Dependencies
├── Pipfile / Pipfile.lock # Pipenv dependency files
├── run_app.bat # Windows startup script
└── README.md # Project documentation

---

🚀 How to Run (Quick Start)
The easiest way:  
👉 **Just double-click `run_app.bat`**  

This will:  
1. Start the Django backend server (`http://127.0.0.1:8000`)  
2. Start the agent (`agent.py`) to collect system/process data  
3. Open the frontend dashboard in your browser  

---

🚀 How to Run (in VS Code / Code Editor)

### 🧱 Step 1: Setup Backend (Django)
```bash
# Create virtual environment (optional)
pipenv shell

# Install dependencies
pip install -r requirements.txt

# Run server
python manage.py runserver
Server will start at: http://127.0.0.1:8000

🤖 Step 2: Run Agent Script
pipenv shell
cd agent
python agent.py

This will collect system process data and upload it to the backend every 5 seconds.

🛠️ Technologies Used

Backend: Django, Django REST Framework
Agent: Python (psutil)
Database: SQLite
Frontend: HTML, CSS, JavaScript

📜 License
This project is built for professional evaluation purposes and intended to demonstrate real-world Django development skills. Usage beyond this scope is not authorized without prior consent.

👨‍💻 Author
Mahin Qureshi
Backend & Fullstack Enthusiast
🔗 LinkedIn:https://www.linkedin.com/in/mahin-qureshi-932b07237/
💻 GitHub:https://github.com/Mahin2024/