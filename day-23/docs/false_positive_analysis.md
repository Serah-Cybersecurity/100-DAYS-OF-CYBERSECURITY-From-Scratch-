# False Positive Analysis

---

## Rule 1: Windows Failed Logon Event Observed

### Rule Name
Windows Failed Logon Event Observed (`rules/windows/windows_failed_logon_event.yml`, ID: `f5347a96-10c0-45f1-a984-b527db7ae9d9`, Level: `low`)

### Intended Behaviour
Identifies Windows Security failed logon events (`EventID: 4625`, converted to `source="WinEventLog:Security" EventCode=4625` in Splunk SPL) as a low-level indicator that warrants contextual review rather than standing alone as a confirmed compromise.

### Possible Legitimate Explanations
- A user mistyped their password during an interactive or remote sign-in.
- A recent password change was not yet updated across an active session, mapped drive, or mobile/workstation client.
- A scheduled task, script, or service used expired or rotated credentials.
- A misconfigured application attempted to authenticate with incorrect credentials.

### Expected Noise Sources
- Morning login typos across workstations during shift changes or peak hours.
- Stale saved credentials on endpoints or service accounts after password rotation.
- Routine authentication retries from background tools or misconfigured integrations.

### Required Investigation Context
- Target account name (`AccountName` / `TargetUserName`) and whether it is a standard user, privileged account, or service account.
- Source workstation/host (`Computer`), source IP/network, and logon type context.
- Frequency and timing pattern (an isolated one-off failure vs. rapid repeated failures or wide horizontal spraying across accounts/hosts).
- Follow-on events around the same timeframe, such as a subsequent successful logon (`4624`) or account lockout (`4740`).

### Tuning Considerations
- Correlate multiple `4625` events over time or group by source/target/host to highlight brute-force or password-spraying patterns instead of alerting heavily on every single raw event.
- Scope higher-priority triage to sensitive accounts or critical servers while keeping standalone raw `4625` visibility low-severity or hunt/triage-oriented.
- Only exempt verified, tightly documented service/automation accounts after confirming no active risk.

### Risks of Over-Tuning
- Broadly allow-listing entire IP ranges/subnets, workstations, or shared service accounts can let an attacker blend brute-force or credential-stuffing traffic into trusted noise.
- Suppressing too aggressively can hide early reconnaissance or slow password spraying before lockouts occur.

---

## Rule 2: Windows Account Lockout Event Observed

### Rule Name
Windows Account Lockout Event Observed (`rules/windows/windows_account_lockout_event.yml`, ID: `8a365057-89cc-457c-b1d6-fb08df7dc6be`, Level: `medium`)

### Intended Behaviour
Identifies Windows Security account lockout events (`EventID: 4740`, converted to `source="WinEventLog:Security" EventCode=4740` in Splunk SPL) at `medium` severity because an account reached the lockout threshold—impacting user availability and potentially signaling automated or repeated failed sign-in attempts.

### Possible Legitimate Explanations
- A user repeatedly entered an incorrect password across one or more sign-in prompts.
- An application, background process, or device cached outdated credentials after a password reset and kept retrying until the lockout threshold hit.
- Legitimate account administration or policy/status changes occurred during routine IT operations.

### Expected Noise Sources
- Users locking their own accounts during busy hours or after forgetting a newly set password.
- Cached credentials on workstations, phones, or background sessions after scheduled password rotations.
- Routine helpdesk or directory/account management activity.

### Required Investigation Context
- Locked-out account (`AccountName` / `TargetUserName`), affected workstation/host (`Computer`), and any caller/source machine details present in the event.
- Preceding `4625` failed logon events—how many occurred, from which sources/hosts, and over what time window.
- Whether the user recently changed their password, is traveling/remote, or reported being locked out, plus whether any `4624` successful logons occurred before or after.

### Tuning Considerations
- Pair `4740` alerts with surrounding `4625` (failed logon) and `4624` (successful logon) timelines during investigation to separate accidental credential staleness from targeted lockouts or denial-of-service attempts.
- Track repeat lockouts for the same account or workstation to spot recurring misconfigurations or active targeting.
- Document known administrative workflows so analysts can quickly rule out expected operational changes.

### Risks of Over-Tuning
- Ignoring or suppressing `4740` events can leave users stuck without access longer and blind analysts to targeted account lockout (denial-of-access) attempts or brute-force campaigns that cross the lockout threshold.
- Over-filtering by host or account can miss repeated lockouts on high-value or privileged identities.

---

## Rule 3: Windows Authentication Events of Interest

### Rule Name
Windows Authentication Events of Interest (`rules/windows/windows_authentication_events_of_interest.yml`, ID: `c528c8d9-782b-46cb-9800-ba5042d55ce0`, Level: `informational`)

### Intended Behaviour
Broadly captures selected Windows Security authentication events where `EventID` is `4624` OR `4625` (converted to `source="WinEventLog:Security" (EventCode IN (4624, 4625))` in Splunk SPL) at `informational` level to support baseline visibility, timeline reconstruction, and correlation rather than acting as a standalone high-severity alert.

### Possible Legitimate Explanations
- Everyday successful user and system logons (`4624`) across workstations, servers, and background services.
- Routine or occasional failed logons (`4625`) from typos, credential updates, or background processes.
- Normal authentication activity generated continuously across an active Windows environment.

### Expected Noise Sources
- High-volume `4624` events from regular user logins, scheduled tasks, service logons, and administrative/monitoring sessions.
- Ongoing `4625` events from minor user typos or stale credentials.
- High overall event volume—because `4624 OR 4625` is intentionally broad, treating it as a high-severity alert without context or aggregation would generate heavy benign volume.

### Required Investigation Context
- Specific `EventID` (`4624` vs. `4625`), `AccountName`, and `Computer` for every matched event.
- Sequence and correlation across events—for example, a burst of `4625` failures followed by a `4624` success on the same account or host, or unusual timing/host pairs.
- Baseline expectations for the account and workstation (normal hours, usual hosts, and expected authentication flow).

### Tuning Considerations
- Keep this broad `4624 OR 4625` rule at `informational` / investigative level or use it for correlation, filtering, and timeline context rather than high-severity alerting.
- Narrow or aggregate in downstream queries (such as filtering by specific logon types, accounts, hosts, or time windows) when hunting for specific behaviors like brute-force-then-success chains.
- Avoid turning an unfiltered `4624 OR 4625` match into a noisy paging alert.

### Risks of Over-Tuning
- Adding broad exclusions to a general `4624 OR 4625` rule can strip away crucial context needed to reconstruct how an attacker moved or authenticated before/after suspicious activity.
- Filtering out too much `4624` or `4625` data at the collection/query stage can break timeline visibility during incident response.
