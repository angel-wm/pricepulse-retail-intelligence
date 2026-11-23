$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $projectRoot '.venv\Scripts\python.exe'
$runDirectory = Join-Path $projectRoot 'data\scheduled'
if (-not (Test-Path -LiteralPath $pythonPath)) { throw 'Project virtual environment is missing.' }
$process = Start-Process -FilePath $pythonPath -ArgumentList @('-m', 'pricepulse.scheduled', '--directory', ('"' + $runDirectory + '"')) -WorkingDirectory $projectRoot -WindowStyle Hidden -Wait -PassThru
exit $process.ExitCode
