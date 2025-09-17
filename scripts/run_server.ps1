param(
    [int]$Port = 8000
)

# Ensure logs dir
$logs = Join-Path -Path $PSScriptRoot -ChildPath '..\logs'
if (-not (Test-Path $logs)) { New-Item -ItemType Directory -Path $logs | Out-Null }

$venvPython = Join-Path -Path $PSScriptRoot -ChildPath '..\.venv\Scripts\python.exe'
if (-not (Test-Path $venvPython)) { Write-Error "Venv python not found at $venvPython"; exit 1 }

$out = Join-Path $logs "uvicorn_out.txt"
$err = Join-Path $logs "uvicorn_err.txt"

Write-Output "Starting uvicorn on port $Port (logs: $out, $err)"

Start-Process -FilePath $venvPython -ArgumentList "-m uvicorn main:app --host 127.0.0.1 --port $Port" -RedirectStandardOutput $out -RedirectStandardError $err -WindowStyle Hidden

Write-Output "Server started (detached). Use Get-Content $out -Wait to follow logs."
