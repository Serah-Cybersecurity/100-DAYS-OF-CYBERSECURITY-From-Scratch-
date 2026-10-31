# PowerShell Event Log Querying & Triage Guide - Day 12

## Primary Cmdlets
* `Get-WinEvent`: Modern, high-performance cmdlet for querying local and remote Windows event logs via structured filters.
* `Get-EventLog`: Legacy cmdlet (deprecated in PowerShell Core/7+), limited to standard classic logs.

## High-Performance Filtering via `-FilterHashtable`
Avoid piping `Get-WinEvent` to `Where-Object`. Use `-FilterHashtable` to perform database-level filtering directly within the event log engine:

```powershell
# High Performance (Database-level filtering)
Get-WinEvent -FilterHashtable @{
    LogName   = 'Security'
    Id        = 4624
    StartTime = (Get-Date).AddHours(-24)
}
