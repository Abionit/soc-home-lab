param(
    [string]$Version = "v4.14.4",
    [string]$Destination = ".\vendor\wazuh-docker"
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path ".\vendor" | Out-Null

if (-not (Test-Path $Destination)) {
    $zipPath = ".\vendor\wazuh-docker-$Version.zip"
    $downloadUrl = "https://github.com/wazuh/wazuh-docker/archive/refs/tags/$Version.zip"

    Write-Host "Downloading Wazuh Docker $Version..."
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath

    Write-Host "Extracting archive..."
    Expand-Archive -Path $zipPath -DestinationPath ".\vendor" -Force
    Move-Item -Path ".\vendor\wazuh-docker-$($Version.TrimStart('v'))" -Destination $Destination -Force
}

Write-Host "Wazuh Docker files are ready at $Destination"
Write-Host "Next steps:"
Write-Host "  cd $Destination\single-node"
Write-Host "  docker compose -f generate-indexer-certs.yml run --rm generator"
Write-Host "  docker compose up -d"
