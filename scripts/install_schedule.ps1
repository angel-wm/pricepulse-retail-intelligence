$ErrorActionPreference = 'Stop'
$taskName = 'PricePulse-Local-Collect'
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) { throw "Task $taskName already exists; inspect it before making changes." }
$tickPath = Join-Path $PSScriptRoot 'scheduled_tick.ps1'
$next = (Get-Date).Date.AddHours((Get-Date).Hour).AddMinutes(20)
if ($next -le (Get-Date)) { $next = $next.AddHours(1) }
$trigger = New-ScheduledTaskTrigger -Once -At $next -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 3650)
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument ('-NoProfile -NonInteractive -WindowStyle Hidden -File "' + $tickPath + '"')
$principal = New-ScheduledTaskPrincipal -UserId ([System.Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 30)
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description 'PricePulse collection-only tick; once daily after 12:15 Europe/Zagreb while user is logged on.'
