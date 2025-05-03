# run.ps1

# Go to project directory
cd "C:\Users\HOME\Desktop\django_crash\Dev\trydjango\lapaulla_store"

# Set Django settings module
$env:DJANGO_SETTINGS_MODULE = "lapaulla_store.settings"

# Path to virtual environment activation script
$venvActivate = "..\myvenv\Scripts\Activate.ps1"

# Activate virtual environment if not already active
if (-not ($env:VIRTUAL_ENV)) {
    if (Test-Path $venvActivate) {
        & $venvActivate
    } else {
        Write-Host "WARNING: Could not find virtual environment activate script at '$venvActivate'"
    }
} else {
    Write-Host "Virtual environment already active."
}

# Run the Django server
python manage.py runserver
