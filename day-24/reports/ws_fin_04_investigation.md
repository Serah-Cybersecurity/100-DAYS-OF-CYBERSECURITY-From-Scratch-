# Day 24 Lab B Investigation Report — Workstation WS-FIN-04

## Summary Counts (Synthetic Dataset: `ws_fin_04_events.jsonl`)
- **Total valid records:** 6 (`09:01:00Z` to `09:10:00Z` UTC)
- **Total invalid records:** 0
- **Event ID counts:** `4625`: 2, `4624`: 1, `1`: 1, `3`: 1, `1102`: 1
- **Logon totals:** 2 failed logons (`4625`), 1 successful logon (`4624`)

## Chronological Timeline (UTC)
1. `2026-11-25T09:01:00Z` | `WS-FIN-04` | `Security` | Event ID `4625` | `user_a` | `source_ip=203.0.113.45` — Failed logon
2. `2026-11-25T09:02:00Z` | `WS-FIN-04` | `Security` | Event ID `4625` | `user_a` | `source_ip=203.0.113.45` — Failed logon
3. `2026-11-25T09:03:00Z` | `WS-FIN-04` | `Security` | Event ID `4624` | `user_a` | `source_ip=203.0.113.45` — Successful logon
4. `2026-11-25T09:04:00Z` | `WS-FIN-04` | `Sysmon` | Event ID `1` | `user_a` | `process_name=sample.exe`, `parent_process=explorer.exe` — Sysmon process creation
5. `2026-11-25T09:05:00Z` | `WS-FIN-04` | `Sysmon` | Event ID `3` | `user_a` | `process_name=sample.exe`, `destination_ip=198.51.100.70` — Synthetic network connection
6. `2026-11-25T09:10:00Z` | `WS-FIN-04` | `Security` | Event ID `1102` | `user_a` — Audit log cleared

## Observed Facts (Strictly From the Six Records)
- All six synthetic records originate from host `WS-FIN-04` between `09:01:00Z` and `09:10:00Z` and reference `user_a`.
- Two `Security` Event ID `4625` (failed logon) entries occurred at `09:01:00Z` and `09:02:00Z` for `user_a` with `source_ip` `203.0.113.45` (TEST-NET-3 documentation IP).
- One `Security` Event ID `4624` (successful logon) entry occurred at `09:03:00Z` for `user_a` with `source_ip` `203.0.113.45`.
- One `Sysmon` Event ID `1` (process creation) entry occurred at `09:04:00Z` under `user_a` showing `process_name` `sample.exe` with `parent_process` `explorer.exe`.
- One `Sysmon` Event ID `3` (network connection) entry occurred at `09:05:00Z` under `user_a` showing `process_name` `sample.exe` and `destination_ip` `198.51.100.70` (TEST-NET-2 documentation IP).
- One `Security` Event ID `1102` (audit log cleared) entry occurred at `09:10:00Z` under `user_a`, five minutes after the Event ID `3` record.

## Investigative Hypotheses (Unproven — Require Verification)
- **Authentication hypothesis:** The two failed logons followed by a successful logon from `203.0.113.45` could reflect benign credential retries/typos by `user_a` or unauthorized authentication attempts preceding a valid session; temporal order alone does not prove causation.
- **Process & network hypothesis:** `sample.exe` spawned by `explorer.exe` and connecting to `198.51.100.70` could represent an authorized test/administrative/user tool or unwanted/malicious software; neither the filename `sample.exe` nor the example IP `198.51.100.70` proves intent on its own.
- **Log-clearing hypothesis:** Event ID `1102` at `09:10:00Z` could result from routine administrative maintenance, log policy/reconfiguration testing, or an attempt to obscure prior activity; its motive cannot be determined from this single event alone.

## Missing Evidence Needed
- **Authentication details:** Logon type, failure status/substatus codes, authentication package, and whether `203.0.113.45` is an expected VPN/jump/corporate address or an unfamiliar source.
- **Process & endpoint telemetry:** Full file path (`Image`), command line (`CommandLine`), file hashes (`Hashes`), `ProcessGuid`, `ParentProcessGuid`, and whether Security Event ID `4688` is enabled alongside Sysmon Event ID `1`.
- **Network context:** Destination port, transport protocol, connection direction, DNS query logs (such as Sysmon Event ID `22`), and firewall/proxy/NetFlow records for `198.51.100.70`.
- **Identity, host & change context:** `user_a`'s role and baseline behavior, `WS-FIN-04`'s role/sensitivity, and any approved maintenance or change tickets around `09:00:00Z–09:15:00Z`.
- **Telemetry completeness:** Confirmation of whether logs were shipped before `09:10:00Z` or if any log gaps/collection filters exist (remembering missing events do not automatically prove non-occurrence).

## Escalation Recommendation & Confidence Statement
- **Recommendation:** Escalate to **SOC / Incident Response triage** for scoped context verification (identity/IP baseline, full process and network telemetry, and maintenance/change ticket review for the `09:10:00Z` Event ID `1102` clear). Do not declare a confirmed compromise from this snippet alone, and do not dismiss the sequence without verification.
- **Confidence Statement:**
  - **Confidence in maliciousness:** **Low-to-moderate**, because the synthetic dataset provides minimal fields and zero confirmed malicious artifacts, hashes, or external threat intelligence.
  - **Confidence that prompt investigation is warranted:** **Moderate-to-high**, because failed-then-successful logons, process creation and outbound network activity under `user_a`, and a Security audit log clear (`1102`) within a 9-minute window warrant timely verification.
