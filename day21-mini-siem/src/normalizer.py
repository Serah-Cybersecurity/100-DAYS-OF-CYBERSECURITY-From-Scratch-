from datetime import datetime

def parse_timestamp(ts_str):
    """Safely parses timestamp strings or falls back to current time."""
    if not ts_str:
        return datetime.utcnow().isoformat() + "Z"
    return ts_str

def normalise_record(record, source_name):
    """
    Normalizes multi-source log records into a unified ECS subset
    and preserves raw log lineage.
    """
    # Extract source-specific IP fields safely across different log types
    src_ip = record.get("source_ip") or record.get("id.orig_h") or record.get("src_ip")
    dst_ip = record.get("destination_ip") or record.get("id.resp_h") or record.get("dst_ip")
    
    # Map source-specific actions into unified ECS actions
    action = "unknown"
    if source_name == "windows":
        event_id = record.get("event_id")
        action = "authentication_failure" if event_id == 4625 else "authentication_success"
    elif source_name == "firewall":
        raw_action = record.get("action", "")
        action = f"network_connection_{raw_action}"

    normalized = {
        "@timestamp": parse_timestamp(record.get("timestamp") or record.get("ts")),
        "event": {
            "provider": source_name,
            "action": action
        },
        "source": {
            "ip": src_ip
        },
        "destination": {
            "ip": dst_ip
        },
        "raw_reference": record  # Preserves complete original log lineage
    }
    return normalized
