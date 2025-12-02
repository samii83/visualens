# backend/start-dev.ps1
# Convenience PS script to start the backend during development.

# Usage: Open a PowerShell terminal and run: .\start-dev.ps1

python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
