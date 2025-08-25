@echo off
SETLOCAL

echo Installing dependencies...
pip install -r requirements.txt

:: Run migrations to ensure all tables exist
echo Applying migrations...
python manage.py migrate

:: Create default superuser if not exists
echo Ensuring default superuser exists...
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','admin@example.com','admin123')"

echo Starting Django server...
start cmd /k "python manage.py runserver 127.0.0.1:8000"

timeout /t 3
echo Starting agent to collect system info...
start cmd /k "python agent/agent.py"

timeout /t 3
echo Opening frontend...
start "" "http://127.0.0.1:8000"

ENDLOCAL

