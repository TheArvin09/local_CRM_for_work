@echo off
echo Starting CRM...
echo.
echo Once you see "Application startup complete", open your browser
echo and go to: http://127.0.0.1:8000
echo.
echo To stop the server - close this window or press Ctrl+C
echo.

call venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

pause
