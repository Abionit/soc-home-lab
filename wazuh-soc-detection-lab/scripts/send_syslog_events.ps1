param(
    [string]$InputFile = ".\output\generated_lab_events.log",
    [string]$Server = "127.0.0.1",
    [int]$Port = 514
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $InputFile)) {
    throw "Input file not found: $InputFile"
}

$udpClient = New-Object System.Net.Sockets.UdpClient
$endpoint = New-Object System.Net.IPEndPoint ([System.Net.IPAddress]::Parse($Server), $Port)

Get-Content $InputFile | ForEach-Object {
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($_)
    [void]$udpClient.Send($bytes, $bytes.Length, $endpoint)
    Start-Sleep -Milliseconds 150
}

$udpClient.Close()
Write-Host "Events sent to $Server`:$Port"
