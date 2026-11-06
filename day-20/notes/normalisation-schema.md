# Network Event Normalisation Schema (Educational ECS Subset)

| Common Field Schema | Suricata Source Field | Zeek Source Field |
| :--- | :--- | :--- |
| `@timestamp` | `timestamp` | `ts` |
| `source.ip` | `src_ip` | `id.orig_h` |
| `source.port` | `src_port` | `id.orig_p` |
| `destination.ip` | `dest_ip` | `id.resp_h` |
| `destination.port` | `dest_port` | `id.resp_p` |
| `network.transport` | `proto` | `proto` |
| `network.community_id` | `community_id` | `community_id` |
| `event.dataset` | Suricata event type | Zeek log name |
| `event.kind` | Alert / event classification | Network event classification |
