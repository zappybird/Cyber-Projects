import json
import csv

def export_json(stats, path):
    with open(path, "w") as f:
        json.dump(stats.to_dict(), f, indent=2)

def export_csv(stats, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Protocol", "Count"])
        for proto, count in stats.protocol_counts.items():
            writer.writerow([proto, count])
