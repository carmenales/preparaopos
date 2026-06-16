$ErrorActionPreference = "Stop"

Write-Host "Checking Docker Compose services..." -ForegroundColor Cyan

docker compose ps

Write-Host ""
Write-Host "Checking web application..." -ForegroundColor Cyan

try {
    $webResponse = Invoke-WebRequest -Uri "http://localhost:8080" -UseBasicParsing -TimeoutSec 10

    if ($webResponse.StatusCode -ne 200) {
        throw "Unexpected status code from web app: $($webResponse.StatusCode)"
    }

    Write-Host "OK - Web application is reachable at http://localhost:8080" -ForegroundColor Green
}
catch {
    Write-Host "ERROR - Web application is not reachable." -ForegroundColor Red
    throw
}

Write-Host ""
Write-Host "Checking phpMyAdmin..." -ForegroundColor Cyan

try {
    $phpMyAdminResponse = Invoke-WebRequest -Uri "http://localhost:8081" -UseBasicParsing -TimeoutSec 10

    if ($phpMyAdminResponse.StatusCode -ne 200) {
        throw "Unexpected status code from phpMyAdmin: $($phpMyAdminResponse.StatusCode)"
    }

    Write-Host "OK - phpMyAdmin is reachable at http://localhost:8081" -ForegroundColor Green
}
catch {
    Write-Host "ERROR - phpMyAdmin is not reachable." -ForegroundColor Red
    throw
}

Write-Host ""
Write-Host "Checking MariaDB tables..." -ForegroundColor Cyan

$tablesOutput = docker compose exec -T db mariadb `
    -h 127.0.0.1 `
    -u preparaopos `
    -ppreparaopos `
    -N `
    -B `
    preparadortai `
    -e "SHOW TABLES;" 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR - Could not query MariaDB tables." -ForegroundColor Red
    Write-Host $tablesOutput
    throw "MariaDB table check failed."
}

$tables = $tablesOutput |
    Where-Object { $_ -and $_.Trim() -ne "" } |
    ForEach-Object { $_.Trim() }

Write-Host "Detected tables:" -ForegroundColor DarkCyan
$tables | ForEach-Object { Write-Host "- $_" }

$requiredTables = @("ptype", "incorrectas", "rtype")

foreach ($table in $requiredTables) {
    if ($tables -notcontains $table) {
        throw "Required table '$table' was not found in database 'preparadortai'."
    }

    Write-Host "OK - Table '$table' exists." -ForegroundColor Green
}

Write-Host ""
Write-Host "Docker stack check completed successfully." -ForegroundColor Green