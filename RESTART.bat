@echo off
echo ========================================
echo  QA AI Automation - Clean Restart
echo ========================================

echo Clearing Python cache...

for /d /r "." %%d in (__pycache__) do (
    if exist "%%d" rd /s /q "%%d"
)

del /s /q "*.pyc" 2>nul

echo Cache cleared!
echo.

echo Deleting previous test screenshots...

if exist storage\runs (
    rmdir /s /q storage\runs
    mkdir storage\runs
)

echo Screenshots cleared!
echo.

echo Starting Flask server...
python -m backend.app

@REM @echo off
@REM echo ========================================
@REM echo  QA AI Automation - Clean Restart
@REM echo ========================================

@REM echo Clearing Python cache...

@REM for /d /r "." %%d in (__pycache__) do (
@REM     if exist "%%d" rd /s /q "%%d"
@REM )

@REM del /s /q "*.pyc" 2>nul

@REM echo Cache cleared!
@REM echo.

@REM echo Starting Flask server...
@REM python -m backend.app