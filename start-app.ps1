# PowerShell script to set up environment and start FastAPI application
# This script handles virtual environment activation, dependency installation,
# environment variable loading, and application startup with proper error handling.

# Exit codes:
# 1: Virtual environment activation failed
# 2: Dependency installation failed
# 3: Application startup failed

# Set error action preference to stop execution on error
$ErrorActionPreference = "Stop"

# Function to load environment variables from .env file
function Load-DotEnv {
    param (
        [string]$Path = ".env"
    )

    if (Test-Path $Path) {
        Write-Host "Loading environment variables from $Path..."
        Get-Content $Path | ForEach-Object {
            $line = $_.Trim()
            if ($line -and !$line.StartsWith("#")) {
                $parts = $line -split '=', 2
                if ($parts.Count -eq 2) {
                    $key = $parts[0].Trim()
                    $value = $parts[1].Trim()
                    [Environment]::SetEnvironmentVariable($key, $value, "Process")
                    Write-Host "Set environment variable: $key"
                } else {
                    Write-Warning "Skipped invalid line: $line"
                }
            }
        }
    } else {
        Write-Warning ".env file not found at path '$Path'. Using system environment variables."
    }
}
# Step 1: Activate virtual environment
try {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    
    # Check if virtual environment exists
    if (-not (Test-Path ".venv")) {
        Write-Host "Virtual environment '.venv' not found. Creating a new one..." -ForegroundColor Yellow
        python -m venv venv
    }
    
    # Activate virtual environment
    & .\.venv\Scripts\Activate.ps1
    
    Write-Host "Virtual environment activated successfully." -ForegroundColor Green
} catch {
    Write-Host "Error: Failed to activate virtual environment:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "Please ensure Python is installed and you have permission to create virtual environments." -ForegroundColor Red
    exit 1
}

# Step 2: Install dependencies
try {
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Cyan
    
    # Check if requirements.txt exists
    if (-not (Test-Path "requirements.txt")) {
        Write-Host "Warning: requirements.txt not found. Skipping dependency installation." -ForegroundColor Yellow
    } else {
        pip install -r requirements.txt
        Write-Host "Dependencies installed successfully." -ForegroundColor Green
    }
} catch {
    Write-Host "Error: Failed to install dependencies:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "Please check your internet connection and requirements.txt file." -ForegroundColor Red
    exit 2
}

# Step 3: Load environment variables from .env file
try {
    Load-DotEnv
    Write-Host "Environment variables loaded successfully." -ForegroundColor Green
} catch {
    Write-Host "Warning: Failed to load some environment variables:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    Write-Host "Continuing with available environment variables..." -ForegroundColor Yellow
}

# Step 4: Start the FastAPI application
try {
    Write-Host "Starting FastAPI application..." -ForegroundColor Cyan
    
    # Run uvicorn to start the application
    uvicorn app.main:app --host 0.0.0.0 --port 8000
    
    Write-Host "Application started successfully." -ForegroundColor Green
} catch {
    Write-Host "Error: Failed to start the FastAPI application:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "Please check that uvicorn is installed and app/main.py exists with a valid FastAPI app instance." -ForegroundColor Red
    exit 3
}

