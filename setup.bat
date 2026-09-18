@echo off
echo ===================================
echo   Настройка CRM - подождите...
echo ===================================
echo.

REM Шаг 1: создание виртуального окружения
echo [1/5] Создаю виртуальное окружение...
python -m venv venv
if errorlevel 1 (
    echo ОШИБКА: не удалось создать venv. Проверьте, что Python установлен и добавлен в PATH.
    pause
    exit /b
)

REM Шаг 2: активация venv и установка зависимостей
echo [2/5] Устанавливаю зависимости...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ОШИБКА: не удалось установить зависимости.
    pause
    exit /b
)

REM Шаг 3: создание .env файла
echo [3/5] Создаю файл настроек...
(
echo DB_HOST=localhost
echo DB_PORT=5432
echo DB_USER=admin
echo DB_PASS=admin123
echo DB_NAME=crm_db
) > .env

REM Шаг 4: создание пользователя и базы данных в Postgres
echo [4/5] Настраиваю базу данных...
echo Сейчас потребуется ввести пароль администратора Postgres
echo (тот, что вы задали при установке PostgreSQL)
echo.

set PSQL=
for %%v in (18 17 16 15 14 13) do (
    if exist "C:\Program Files\PostgreSQL\%%v\bin\psql.exe" set PSQL=C:\Program Files\PostgreSQL\%%v\bin\psql.exe
)

if "%PSQL%"=="" (
    echo Не удалось найти psql.exe автоматически.
    echo Найдите файл psql.exe в папке PostgreSQL ^(обычно в C:\Program Files\PostgreSQL\ВЕРСИЯ\bin^)
    echo и сообщите путь к нему для настройки.
    pause
    exit /b
)

echo Найден psql: %PSQL%
"%PSQL%" -U postgres -c "CREATE USER admin WITH PASSWORD 'admin123';"
"%PSQL%" -U postgres -c "CREATE DATABASE crm_db OWNER admin;"

REM Шаг 5: применение миграций
echo [5/5] Создаю таблицы в базе данных...
alembic upgrade head
if errorlevel 1 (
    echo ОШИБКА: не удалось применить миграции.
    pause
    exit /b
)

echo.
echo ===================================
echo   Готово! Настройка завершена.
echo   Теперь запустите start.bat
echo ===================================
pause
