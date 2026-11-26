# Hands-On Triage Note — WS-FIN-04

## 1. Alert Validation
- Host: WS-FIN-04 | Account: user_a | Channels: Security, Sysmon | Window: 2026-11-25T09:01:00Z to 09:10:00Z (UTC)

## 2. Data Quality Check
- Timestamps are in ISO-8601 UTC (`Z`); 6 valid records, 0 quarantined records in synthetic dataset.
- Event ID 1102 appears at 09:10:00Z; potential log gaps or missing audit fields must be verified on real telemetry.

## 3. Timeline & Gaps
- 09:01:00Z (4625 failed logon, 203.0.113.45) -> 09:02:00Z (4625 failed logon, 203.0.113.45) -> 09:03:00Z (4624 successful logon, 203.0.113.45) -> 09:04:00Z (Sysmon 1: sample.exe from explorer.exe) -> 09:05:00Z (Sysmon 3: sample.exe -> 198.51.100.70) -> 5-minute gap -> 09:10:00Z (1102 audit log cleared).

## 4. Correlation Notes
- All 6 records share host WS-FIN-04 and username user_a; source IP 203.0.113.45 links the 4625/4624 events, and process_name sample.exe links the Sysmon 1 and Sysmon 3 events. ProcessGuid, LogonId, ports, and hashes are not present in this synthetic snippet.

## 5. Alternative Explanations
- Benign/operational: user_a credential retries, legitimate tool/test execution via explorer.exe, and routine log maintenance/reconfiguration.
- Suspicious/malicious: unauthorized login attempts followed by unauthorized tooling, outbound communication, and log clearing.

## 6. Known / Suspected / Unknown / Next Steps
- Known: The exact 6 events, timestamps, IPs, process/parent names, and account above.
- Suspected: Unverified benign or malicious causes for the auth sequence, sample.exe activity, and 1102 clear.
- Unknown: Logon type, status/substatus codes, full Image path, CommandLine, file hashes, ProcessGuid/LogonId, destination port/DNS/proxy/firewall context, user/host role, and change tickets.
- Next Steps: Pivot to full endpoint/network/identity/change-ticket telemetry before drawing a compromise conclusion.

## 7. Escalation & Authorization
- Escalate to Tier 2 / IR with this structured record for scoped verification; do not execute disruptive containment actions without explicit authorization.
