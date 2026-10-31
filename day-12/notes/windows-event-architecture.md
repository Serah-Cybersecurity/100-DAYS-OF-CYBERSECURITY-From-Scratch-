# Windows Event Log Architecture Notes - Day 12

## Core Architecture
* **Format:** Proprietary structured XML binary format (`.evtx`) stored in `C:\Windows\System32\winevt\Logs\`.
* **GUI Tool:** Windows Event Viewer (`eventvwr.msc`).

## The Five Primary Windows Event Channels
1. **System:** Operating system driver, hardware, system startup/shutdown, and service state events.
2. **Security:** Authentication, process creation, object access, user rights assignments, and audit log state changes (requires administrative access).
3. **Application:** System component, third-party application, and database event messages.
4. **Setup:** Operating system installation, feature additions, and Windows Update events.
5. **ForwardedEvents:** Centralized event collection from remote endpoints via Windows Event Forwarding (WEF).
