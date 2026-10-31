# Security & System Event ID Reference - Day 12

## Core Security Event Identifiers
* **Event ID 4624 (Security):** An account was successfully logged on. Key fields: `TargetUserName`, `LogonType` (Type 2 = Interactive, Type 3 = Network, Type 5 = Service, Type 10 = RemoteDesktop), `LogonId`, `IpAddress`.
* **Event ID 4625 (Security):** An account failed to log on. Key fields: `TargetUserName`, `FailureReason`, `SubStatus`, `IpAddress`.
* **Event ID 4672 (Security):** Special privileges assigned to new logon (e.g., `SeDebugPrivilege`, `SeBackupPrivilege`).
* **Event ID 4688 (Security):** A new process has been created. Key fields: `NewProcessName`, `CommandLine`, `ParentProcessName`, `SubjectLogonId`.
* **Event ID 1102 (Security):** The audit log was cleared (primary anti-forensics / adversary tampering indicator).

## System Service Events
* **Event ID 7045 (System):** A service was installed in the system (frequently used for persistence and privilege escalation).
