@echo off
echo Запускаю CRM...
echo.
echo Когда увидите "Application startup complete", откройте браузер
echo и перейдите на адрес: http://127.0.0.1:8000
echo.
echo Чтобы остановить сервер - закройте это окно или нажмите Ctrl+C
echo.

call venv\Scripts\activate.bat
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

pause
