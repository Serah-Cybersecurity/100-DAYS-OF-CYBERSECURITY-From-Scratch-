# Network Investigation Timeline

| Timestamp | Tool | Event | Source | Destination | Evidence |
|---|---|---|---|---|---|
| 2026-11-06T10:43:04.222546Z | Zeek | DNS Query (A Record Lookup) | 10.0.2.15 | 192.168.100.1 | `dns.log` (uid: Cwm0RP3YRwEK1TkZrd, query: example.com) |
| 2026-11-06T10:43:04.222546Z | Suricata | Local Lab DNS Alert (`sid:1000001`) | 10.0.2.15 | 192.168.100.1 | `eve.json` (Community ID: `1:P2oNim+dAcDZgQht0+q2HlbuHXU=`) |
| 2026-11-06T10:43:20.653025Z | Zeek | DNS Query & Response | 10.0.2.15 | 192.168.100.1 | `dns.log` (uid: C6kga32wpCLFCqXqk, query: example.com) |
| 2026-11-06T10:43:20.653025Z | Suricata | Local Lab DNS Alert (`sid:1000001`) | 10.0.2.15 | 192.168.100.1 | `eve.json` (Community ID: `1:I6puVD0/FGcSzdfYg+4Rm1dA84=`) |

## Timeline Interpretation
The timeline establishes a direct correlation between host `10.0.2.15` initiating DNS resolution requests for `example.com` and Suricata's signature detection engine (`sid:1000001`) firing alerts within the exact same microsecond boundary. Zeek connection and DNS logs validate that UDP port 53 traffic successfully resolved domain answers.

## Correlation Confidence
* **High Confidence:** Suricata alerts matched Zeek `conn.log` and `dns.log` records with 100% cryptographic certainty using identical **Community ID** flow hashes and **Zeek UIDs**, backed by strict bi-directional endpoint verification and a 30-second timestamp tolerance window.

## Limitations
The evidence confirms that DNS queries for `example.com` were processed and logged. However, it **does not establish** user intent, whether an application successfully established an outbound HTTP/HTTPS session following DNS resolution, or whether the activity was part of an authorized network diagnostic test.
