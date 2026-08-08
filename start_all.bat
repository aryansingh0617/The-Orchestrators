@echo off
echo Starting Project Chimera (Frontend + Backend)...
start "Chimera Backend" cmd /k "cd backend && start_backend.bat"
start "Chimera Frontend" cmd /k "cd frontend && npm run dev"
