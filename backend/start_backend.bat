@echo off
echo Starting Project Chimera Backend...
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload
