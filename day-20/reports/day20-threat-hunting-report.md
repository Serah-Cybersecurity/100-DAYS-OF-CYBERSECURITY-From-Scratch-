# Day 20: Integrated Threat Hunting Report

## Objective
Correlate Suricata EVE JSON logs with Zeek network logs using Community ID flow hashes.

## Findings
- **PCAP File:** `day20.pcap`
- **Community ID:** `1:HxMkRMSXRcDEXn0KQrmp0iwucCw=`
- **Matched Traffic:** DNS query and response sessions to `2.debian.pool.ntp.org`.
- **Correlation Status:** Successfully mapped Suricata EVE alerts to corresponding session records in Zeek.
