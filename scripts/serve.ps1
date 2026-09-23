# Start local static server for DAAB site (required for http://127.0.0.1:8010 preview).
$Port = 8010
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root
Write-Host "DAAB static server: http://127.0.0.1:$Port/az/index.html"
Write-Host "Press Ctrl+C to stop."
python helpers/serve_site.py --bind 127.0.0.1 --port $Port
