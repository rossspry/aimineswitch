# Creates a distributable zip next to this repo (Windows usage)
param(
  [string]$Version = "dev"
)
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$zip = Join-Path $repo "..\AIMineSwitch-$Version.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
# Exclude common junk
$excludes = @('.git', '.github', 'venv', '.venv', '__pycache__', '*.pyc')
Add-Type -AssemblyName System.IO.Compression.FileSystem
function Add-ToZip($zipPath, $sourcePath) {
  if (-Not (Test-Path $zipPath)) {
    [System.IO.Compression.ZipFile]::CreateFromDirectory($sourcePath, $zipPath)
  } else {
    [System.IO.Compression.ZipFile]::CreateFromDirectory($sourcePath, $zipPath)
  }
}
# Use PowerShell's Compress-Archive for simplicity
$items = Get-ChildItem $repo -Force | Where-Object { $_.Name -notin $excludes }
Compress-Archive -Path $items.FullName -DestinationPath $zip -Force
Write-Host "Created $zip"
