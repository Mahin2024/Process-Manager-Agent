@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo Starting Django server...
start cmd /k "python manage.py runserver 127.0.0.1:8000"

timeout /t 3
echo Starting agent to collect system info...
start cmd /k "python agent/agent.py"

timeout /t 3
echo Opening frontend...
start "" "http://127.0.0.1:8000"
