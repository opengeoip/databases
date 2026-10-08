import json
import sys

BREAKDOWNS = [("network", "Network"), ("continent", "Continent")]
LABELS = {
    "access": "Access (Cable/DSL/ISP)",
    "transit": "Transit (NSP)",
    "content": "Content and hosting",
    "other": "Other",
    "unknown": "Not in PeeringDB",
    "unrouted": "No AS in Atlas",
}


def cell(result):
    if result is None:
        return "–"
    return f'{result["databases"][0]["accuracy"]:.2f} % ({result["probes"]})'


def main(path):
    with open(path) as f:
        results = json.load(f)["results"]
    for by, title in BREAKDOWNS:
        rows = {}
        for result in results:
            if result["by"] == by:
                rows.setdefault(result["group"], {})[result["family"]] = result
        print(f"| {title} | IPv4 | IPv6 |")
        print("|---|---|---|")
        for group, families in rows.items():
            print(f"| {LABELS.get(group, group)} | {cell(families.get('IPv4'))} | {cell(families.get('IPv6'))} |")
        print()


if __name__ == "__main__":
    main(sys.argv[1])
