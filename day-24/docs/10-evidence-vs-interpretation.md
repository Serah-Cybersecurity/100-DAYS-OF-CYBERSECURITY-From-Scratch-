# 10.1 Evidence vs. Interpretation — WS-FIN-04 Exercise

## Example A: Authentication Events (4625 -> 4625 -> 4624)
- **Observation:** `ws_fin_04_events.jsonl` contains two `Security` Event `4625` records (`2026-11-25T09:01:00Z` and `09:02:00Z`) and one `Security` Event `4624` record (`09:03:00Z`) on `WS-FIN-04` for `user_a` with `source_ip` `203.0.113.45`.
- **Interpretation:** These events represent two failed logon records followed by a successful logon record in the telemetry; logon type, failure reason codes, and authentication package are not present in this dataset.
- **Hypothesis:** `user_a` may have mistyped credentials before logging in legitimately, or an unauthorized actor may have attempted access prior to a valid or compromised session.

## Example B: Process, Network, and Audit Clear (Sysmon 1, Sysmon 3, Security 1102)
- **Observation:** The file records Sysmon Event `1` (`sample.exe`, parent `explorer.exe`, `user_a`, `09:04:00Z`), Sysmon Event `3` (`sample.exe`, `destination_ip` `198.51.100.70`, `user_a`, `09:05:00Z`), and Security Event `1102` (`user_a`, `09:10:00Z`).
- **Interpretation:** Telemetry reflects a process start, an outbound network connection record tied to that process name, and a Security log-cleared event five minutes later, without command lines, hashes, ports, or `ProcessGuid` fields in the snippet.
- **Hypothesis:** Activity could stem from authorized user/admin testing and routine log maintenance, or from unauthorized tooling and anti-forensic log clearing.
