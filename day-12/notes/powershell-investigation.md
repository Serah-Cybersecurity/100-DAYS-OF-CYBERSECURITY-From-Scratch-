# PowerShell Event Log Querying & Triage Guide

## 1. What PowerShell Is
PowerShell is an object-oriented task automation engine and command-line shell developed by Microsoft. Unlike traditional shells that output raw text, PowerShell processes inputs and outputs as structured .NET objects, making it ideal for event log analysis, script automation, and endpoint triage.

## 2. What `Get-WinEvent` Does
`Get-WinEvent` is a modern, high-performance PowerShell cmdlet used to query classic Windows event logs, ETW (Event Tracing for Windows) logs, and `.evtx` log files from local or remote computers.

## 3. How `-LogName` Works
The `-LogName` parameter specifies the target event log channel to query (e.g., `System`, `Application`, `Security`).
* **Actual Command Used:**
  ```powershell
  Get-WinEvent -LogName "System" -MaxEvents 10
