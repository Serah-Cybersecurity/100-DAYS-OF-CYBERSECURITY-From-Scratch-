# Day 8 - Authentication Log Analysis & System Telemetry Report

## Overview
Investigated system logging architecture, verified log file paths under `/var/log/`, and explored package manager logging (`dpkg.log`) inside the Parrot OS environment.

## Log Audit & Environmental Findings

### 1. Log File Availability (`/var/log/`)
* **Checked Paths:** `/var/log/auth.log` and `/var/log/secure` returned "No such file or directory"[cite: 29].
* **Analysis:** Operating system distributions handle logging differently. While Debian/Ubuntu derivatives traditionally rely on `auth.log`, modern streamlined builds or containerized environments often route authentication telemetry directly through the systemd journal (`journalctl`) or maintain specialized logs.
* **Alternative Log Discovery:** Inspected `/var/log/` contents and successfully identified active logs such as `dpkg.log` (package installation and system updates) and `boot.log`[cite: 29].

### 2. Package Management Logging (`dpkg.log`)
* **Command Executed:** `less /var/log/dpkg.log`[cite: 28, 29]
* **Observation:** Successfully parsed package installation histories, upgrades, and configuration states with precise timestamps.
* **Security Relevance:** Auditing package logs helps security analysts determine when software packages, tools, or dependencies were added or updated on a system during forensic investigations.
