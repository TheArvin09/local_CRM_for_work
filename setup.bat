@echo off
echo ===================================
echo   CRM Setup - please wait...
echo ===================================
echo.

REM Step 1: create virtual environment
echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: could not create venv. Make sure Python is installed and added to PATH.
    pause
    exit /b
)

REM Step 2: activate venv and install dependencies
echo [2/5] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: could not install dependencies.
    pause
    exit /b
)

REM Step 3: create .env file
echo [3/5] Creating settings file...
(
echo DB_HOST=localhost
echo DB_PORT=5432
echo DB_USER=admin
echo DB_PASS=admin123
echo DB_NAME=crm_db
) > .env

REM Step 4: create Postgres user and database
echo [4/5] Setting up the database...
echo You will be asked for the Postgres admin password now
echo ^(the one you set during PostgreSQL installation^)
echo.

set PSQL=
for %%v in (18 17 16 15 14 13) do (
    if exist "C:\Program Files\PostgreSQL\%%v\bin\psql.exe" set PSQL=C:\Program Files\PostgreSQL\%%v\bin\psql.exe
)

if "%PSQL%"=="" (
    echo Could not find psql.exe automatically.
    echo Look for psql.exe inside C:\Program Files\PostgreSQL\VERSION\bin
    echo and let the project owner know the path so the script can be fixed.
    pause
    exit /b
)

echo Found psql: %PSQL%
"%PSQL%" -U postgres -c "CREATE USER admin WITH PASSWORD 'admin123';"
"%PSQL%" -U postgres -c "CREATE DATABASE crm_db OWNER admin;"

REM Step 5: run migrations
echo [5/5] Creating database tables...
alembic upgrade head
if errorlevel 1 (
    echo ERROR: could not apply migrations.
    pause
    exit /b
)

echo.
echo ===================================
echo   Done! Setup complete.
echo   Now run start.bat
echo ===================================
pause
