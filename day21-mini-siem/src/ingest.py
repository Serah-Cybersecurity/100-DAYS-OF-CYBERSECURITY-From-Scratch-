import json
from pathlib import Path
from src.normalizer import normalise_record
from src.enrichment import load_asset_inventory, enrich_event_with_assets

def run_pipeline():
    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Load asset lookup table
    asset_lookup = load_asset_inventory("data/asset_inventory.json")
    print(f"[+] Loaded {len(asset_lookup)} assets from inventory.")
    
    # Process each raw JSONL log file
    for log_file in raw_dir.glob("*.jsonl"):
        source_name = log_file.stem  # e.g., 'windows', 'firewall', etc.
        output_file = processed_dir / f"normalized_{log_file.name}"
        
        processed_count = 0
        with open(log_file, "r", encoding="utf-8") as infile, \
             open(output_file, "w", encoding="utf-8") as outfile:
            
            for line in infile:
                if not line.strip():
                    continue
                try:
                    raw_event = json.loads(line)
                    # 1. Normalize into ECS subset
                    normalized = normalise_record(raw_event, source_name)
                    # 2. Enrich with asset metadata
                    enriched = enrich_event_with_assets(normalized, asset_lookup)
                    
                    outfile.write(json.dumps(enriched) + "\n")
                    processed_count += 1
                except Exception as e:
                    print(f"[-] Error processing record in {log_file.name}: {e}")
                    
        print(f"[+] Processed {processed_count} events from {source_name} -> {output_file}")

if __name__ == "__main__":
    run_pipeline()
