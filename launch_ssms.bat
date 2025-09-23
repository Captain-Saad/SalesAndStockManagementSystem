@echo off
echo.
echo ================================================
echo   SSMS - Sales & Stock Management System
echo   Ultra-Modern Version 3.0
echo ================================================
echo.
echo Starting application...
echo.

python launch_ssms.py

if %errorlevel% neq 0 (
    echo.
    echo Error occurred. Please check the error message above.
    echo.
    pause
)
