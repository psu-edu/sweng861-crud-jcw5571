$ErrorActionPreference = "Stop"

$certDir = Join-Path $PSScriptRoot "..\certs"

New-Item -ItemType Directory -Force -Path $certDir | Out-Null

# Install mkcert's local CA if it has not already been installed.
mkcert -install

# Generate a certificate for local development.
mkcert `
    -cert-file "$certDir\localhost.pem" `
    -key-file "$certDir\localhost-key.pem" `
    localhost 127.0.0.1 ::1

Write-Host "Development HTTPS certificate generated in $certDir"
