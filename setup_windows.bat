@echo off
REM ResearchPilot Gemini - Windows Setup Script
REM This script creates the .env file and installs dependencies

echo.
echo ========================================
echo ResearchPilot Gemini - Windows Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Step 1: Creating .env file...
(
echo # Required
echo GEMINI_API_KEY=AQ.Ab8RN6Jxf51ZxsSNC4XOyOi9eFXZlFrpkKg_ovbOxlm1SMYuxQ
echo TAVILY_API_KEY=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
echo # Optional
echo GEMINI_MODEL=gemini-2.0-flash
echo MAX_SEARCH_RESULTS=5
echo MAX_QUERIES_PER_ROUND=4
echo MAX_RESEARCH_ROUNDS=2
) > .env

if exist .env (
    echo ✓ .env file created successfully
) else (
    echo ✗ Failed to create .env file
    pause
    exit /b 1
)

echo.
echo Step 2: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ✗ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment created

echo.
echo Step 3: Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated

echo.
echo Step 4: Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

echo.
echo Step 5: Verifying configuration...
python -c "from dotenv import load_dotenv; import os; load_dotenv(); key=os.getenv('GEMINI_API_KEY'); print('✓ GEMINI_API_KEY found' if key else '✗ GEMINI_API_KEY not found')"

echo.
echo ========================================
echo ✓ Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run the Streamlit app:
echo    streamlit run app.py
echo.
echo 2. Or run command-line version:
echo    python main.py
echo.
echo 3. Virtual environment is activated.
echo    To deactivate later, type: deactivate
echo.
pause
