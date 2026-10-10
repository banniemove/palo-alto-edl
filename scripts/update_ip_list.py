#!/usr/bin/env python3
"""Bouwt een IP-lijst (EDL) opnieuw op uit de aangekondigde prefixes (RIPEstat)
van providers met eigen netwerk in een land.

- AS-nummers staan in het asns-bestand (een AS per regel, # = commentaar)
- Prefixes in het exclude-bestand worden overgeslagen
- Veiligheidsrem: als een AS ineens 0 prefixes geeft, of het totaal meer dan
  20% daalt t.o.v. de huidige lijst, wordt er niets overschreven.
"""
import ipaddress
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{asn}&sourceapp=palo-alto-edl"


def read_list(path):
    items = []
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            items.append(line)
    return items


def fetch(asn):
    last_err = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(API.format(asn=asn), timeout=60) as r:
                data = json.load(r)
            if data.get("status") != "ok":
                raise RuntimeError(f"status={data.get('status')}")
            return {ipaddress.ip_network(p["prefix"]) for p in data["data"]["prefixes"]}
        except Exception as e:  # netwerkfout of rate limit: even wachten
            last_err = e
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"AS{asn}: ophalen mislukt: {last_err}")


def main():
    # Gebruik: update_ip_list.py <asns-bestand> <exclude-bestand> <uitvoerbestand>
    if len(sys.argv) != 4:
        sys.exit("Gebruik: update_ip_list.py <asns.txt> <exclude.txt> <ip-list.txt>")
    ASNS_FILE, EXCLUDE_FILE, OUT_FILE = (ROOT / a for a in sys.argv[1:])
    asns = [a.upper().removeprefix("AS") for a in read_list(ASNS_FILE)]
    exclude = {ipaddress.ip_network(p) for p in read_list(EXCLUDE_FILE)}

    prefixes = set()
    for asn in asns:
        nets = fetch(asn)
        if not nets:
            sys.exit(f"AS{asn} geeft 0 prefixes terug - afgebroken, lijst niet gewijzigd.")
        print(f"AS{asn}: {len(nets)} prefixes")
        prefixes |= nets
        time.sleep(1)

    prefixes -= exclude
    out = sorted(prefixes, key=lambda n: (n.version, n))

    if not out:
        sys.exit("Lege lijst - afgebroken.")
    if OUT_FILE.exists():
        old = [l for l in OUT_FILE.read_text().splitlines() if l.strip()]
        if len(out) < 0.8 * len(old):
            sys.exit(f"Nieuwe lijst ({len(out)}) is >20% kleiner dan de oude ({len(old)}) - afgebroken.")

    OUT_FILE.write_text("\n".join(str(n) for n in out) + "\n")
    v4 = sum(n.version == 4 for n in out)
    print(f"Totaal: {len(out)} prefixes ({v4} IPv4, {len(out) - v4} IPv6)")


if __name__ == "__main__":
    main()
