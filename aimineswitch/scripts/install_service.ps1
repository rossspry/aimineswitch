# Configure these paths before running
$svcName = "AIMineSwitch"
$root = "C:\aimineswitch"
$python = (Get-Command python).Source  # Or set explicit path: "C:\Python311\python.exe"
$nssm = "C:\tools\nssm\nssm.exe"    # Set to your NSSM path

& $nssm install $svcName $python "-m" "aimineswitch.service"
& $nssm set $svcName AppDirectory $root
& $nssm set $svcName Start SERVICE_AUTO_START
& $nssm set $svcName AppStopMethodSkip 0
& $nssm start $svcName
Write-Host "Installed and started $svcName"
