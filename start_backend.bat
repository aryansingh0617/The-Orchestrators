@echo off
echo Starting Project Chimera Backend...
call backend\venv\Scripts\activate.bat
python -m uvicorn app.main:app --app-dir backend --reload
