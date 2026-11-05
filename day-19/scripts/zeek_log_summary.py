import json
import sys
from collections import Counter
from pathlib import Path

def read_jsonl(path):
    """
    Read newline-delimited JSON records.
    Returns:
        records: successfully parsed JSON objects
        malformed: number of invalid records
        exists: whether the file was present
    """
    records = []
    malformed = 0
    if not path.exists():
        return records, malformed, False
    
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError:
                malformed += 1
                
    return records, malformed, True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 zeek_log_summary.py <zeek_output_dir>")
        sys.exit(1)
        
    output_dir = Path(sys.argv[1])
    print(f"[*] Analyzing Zeek logs in: {output_dir}")
    
    # 1. Process conn.log
    conn_path = output_dir / "conn.log"
    conn_records, conn_malformed, conn_exists = read_jsonl(conn_path)
    
    proto_counts = Counter()
    service_counts = Counter()
    port_counts = Counter()
    state_counts = Counter()
    
    for r in conn_records:
        if "proto" in r:
            proto_counts[r["proto"]] += 1
        if "service" in r and r["service"]:
            service_counts[r["service"]] += 1
        if "id.resp_p" in r:
            port_counts[r["id.resp_p"]] += 1
        if "conn_state" in r:
            state_counts[r["conn_state"]] += 1
            
    # 2. Process dns.log
    dns_path = output_dir / "dns.log"
    dns_records, dns_malformed, dns_exists = read_jsonl(dns_path)
    
    query_counts = Counter()
    rcode_counts = Counter()
    dns_to_uid = {}
    
    for r in dns_records:
        if "query" in r:
            query_counts[r["query"]] += 1
        if "rcode_name" in r:
            rcode_counts[r["rcode_name"]] += 1
        if "uid" in r and "query" in r:
            dns_to_uid[r["uid"]] = r["query"]
            
    # 3. Process ssl.log
    ssl_path = output_dir / "ssl.log"
    ssl_records, ssl_malformed, ssl_exists = read_jsonl(ssl_path)
    
    tls_versions = Counter()
    server_names = Counter()
    
    for r in ssl_records:
        if "version" in r:
            tls_versions[r["version"]] += 1
        if "server_name" in r and r["server_name"]:
            server_names[r["server_name"]] += 1
            
    # Print Summary Report
    print("\n" + "="*50)
    print(" ZEEK LOG AUTOMATED ANALYSIS REPORT")
    print("="*50)
    print(f"Total Connections: {len(conn_records)} (Malformed: {conn_malformed})")
    print(f"Total DNS Queries: {len(dns_records)} (Malformed: {dns_malformed})")
    print(f"Total SSL Records: {len(ssl_records)} (Malformed: {ssl_malformed})")
    
    print("\n--- Transport Protocols ---")
    for proto, count in proto_counts.most_common():
        print(f"  {proto}: {count}")
        
    print("\n--- Top Destination Ports ---")
    for port, count in port_counts.most_common(5):
        print(f"  Port {port}: {count}")
            
    print("\n--- Connection States ---")
    print(dict(state_counts))
        
    print("\n--- Top DNS Queries ---")
    for q, count in query_counts.most_common(5):
        print(f"  {q}: {count}")
            
    print("\n--- TLS Versions ---")
    print(dict(tls_versions))
        
    print("\n--- Server Names (SNI) ---")
    for sn, count in server_names.most_common(5):
        print(f"  {sn}: {count}")
            
    print("\n--- UID Correlations ---")
    print(f"Successfully correlated {len(dns_to_uid)} DNS sessions with UIDs.")
    print("="*50)

if __name__ == "__main__":
    main()
