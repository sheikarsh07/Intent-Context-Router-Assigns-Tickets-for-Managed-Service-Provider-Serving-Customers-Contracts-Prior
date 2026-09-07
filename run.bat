@echo off
TITLE Intent + Context Ticket Router - One-Click Launcher
CLS

echo ======================================================================
echo    INTENT + CONTEXT TICKET ROUTER FOR MANAGED-SERVICE PROVIDERS
echo ======================================================================
echo.
echo [1/4] Checking and installing Python dependencies...
py -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies. Make sure Python 3.10+ is installed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/4] Generating synthetic datasets (550+ tickets, policies, resolver groups)...
py src/data_generator.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Data generation failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/4] Running automated benchmark evaluation, adversarial tests, and generating Word/PPT docs...
py src/evaluation.py
py tests/test_router.py
py src/generate_documents.py

echo.
echo [4/4] Launching Streamlit Web Application...

echo.
echo Opening app in your default web browser (http://localhost:8501)...
echo Press Ctrl+C in this terminal window to stop the server when done.
echo.
py -m streamlit run app.py

pause
