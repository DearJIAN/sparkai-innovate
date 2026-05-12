$si = New-Object System.Diagnostics.ProcessStartInfo
$si.FileName = "cmd.exe"
$si.Arguments = "/c npm run dev"
$si.WorkingDirectory = "E:\LEAR-CODE-NEW\软件工程\my-keshe\innovation-competition-platform\frontend"
$si.UseShellExecute = $false
$si.CreateNoWindow = $true
[System.Diagnostics.Process]::Start($si) | Out-Null
Write-Output "Frontend start command sent"

Start-Sleep -Seconds 5
netstat -an | Select-String LISTENING | Select-String :5173