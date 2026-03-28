# Jarvis Desktop App - Windows Build Script
# This script builds the Jarvis Desktop application for Windows

param(
    [string]$Configuration = "Release",
    [string]$TargetFramework = "net8.0-windows10.0.19041.0",
    [string]$OutputPath = "bin\publish"
)

Write-Host "Building Jarvis Desktop App for Windows..." -ForegroundColor Green
Write-Host "Configuration: $Configuration" -ForegroundColor Yellow
Write-Host "Target Framework: $TargetFramework" -ForegroundColor Yellow
Write-Host "Output Path: $OutputPath" -ForegroundColor Yellow

# Ensure we're in the project directory
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $projectDir
Set-Location $projectDir

# Restore NuGet packages
Write-Host "Restoring NuGet packages..." -ForegroundColor Cyan
dotnet restore

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to restore NuGet packages"
    exit $LASTEXITCODE
}

# Build the project
Write-Host "Building project..." -ForegroundColor Cyan
dotnet build --configuration $Configuration --framework $TargetFramework --no-restore

if ($LASTEXITCODE -ne 0) {
    Write-Error "Build failed"
    exit $LASTEXITCODE
}

# Publish the application
Write-Host "Publishing application..." -ForegroundColor Cyan
dotnet publish --configuration $Configuration --framework $TargetFramework --output $OutputPath --self-contained true --runtime win-x64

if ($LASTEXITCODE -ne 0) {
    Write-Error "Publish failed"
    exit $LASTEXITCODE
}

# Create installer (optional - requires WiX Toolset or similar)
Write-Host "Creating installer..." -ForegroundColor Cyan

# Copy additional files
Copy-Item "README.md" "$OutputPath\" -ErrorAction SilentlyContinue
Copy-Item "LICENSE" "$OutputPath\" -ErrorAction SilentlyContinue

Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "Output location: $OutputPath" -ForegroundColor Green

# Optional: Create a simple batch file to run the app
$runScript = @"
@echo off
echo Starting Jarvis Desktop App...
start "" "JarvisDesktop.exe"
"@

$runScript | Out-File -FilePath "$OutputPath\RunJarvis.bat" -Encoding UTF8

Write-Host "Run the app using: $OutputPath\RunJarvis.bat" -ForegroundColor Green
