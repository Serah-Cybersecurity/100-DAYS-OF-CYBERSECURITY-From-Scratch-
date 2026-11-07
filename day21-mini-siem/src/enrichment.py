import json
from pathlib import Path

def load_asset_inventory(inventory_path="data/asset_inventory.json"):
    """Loads the local asset inventory into a fast IP lookup dictionary."""
    path = Path(inventory_path)
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        inventory_list = json.load(f)
        # Create a dictionary keyed by IP address for O(1) fast lookups
        return {item["ip"]: item for item in inventory_list if "ip" in item}

def enrich_event_with_assets(normalized_event, asset_lookup):
    """Enriches source IP with asset metadata if found in inventory."""
    src_ip = normalized_event.get("source", {}).get("ip")

    if src_ip in asset_lookup:
        asset_data = asset_lookup[src_ip]
        normalized_event["source"]["asset"] = {
            "hostname": asset_data.get("hostname"),
            "asset_type": asset_data.get("asset_type"),
            "department": asset_data.get("department"),
            "criticality": asset_data.get("criticality")
        }
    else:
        # Graceful handling for unknown/external assets
        normalized_event["source"]["asset"] = {
            "hostname": "unknown",
            "asset_type": "unknown",
            "department": "unknown",
            "criticality": "unknown"
        }

    return normalized_event
