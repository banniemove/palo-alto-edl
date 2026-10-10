#!/usr/bin/env python3
"""Bouwt de IP-lijst (EDL) van een land opnieuw op uit RIPEstat.

Gebruik:  python scripts/update_ip_list.py <landcode>      bijv. nl, fr, de

Per land:
  asns-<cc>.txt     AS-nummers (een per regel, # = commentaar)
  exclude-<cc>.txt  prefixes die eruit blijven (optioneel)
  ip-list-<cc>.txt  uitvoer: een prefix per regel, eerst IPv4 dan IPv6
  reports/<cc>.md   controlerapport: houder, aantal prefixes en geolocatie per AS

Veiligheidsrem: daalt het totaal meer dan 20% t.o.v. de huidige lijst, of is
de lijst leeg, dan wordt er niets overschreven. Een AS met 0 prefixes geeft
een waarschuwing in het rapport.
"""
import datetime
import ipaddress
import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RIPESTAT = "https://stat.ripe.net/data/{call}/data.json?resource=AS{asn}&sourceapp=palo-alto-edl"

# Gebieden die bij een land horen maar in geolocatie een eigen code hebben
EXTRA_CODES = {
    "FR": {"RE", "GP", "MQ", "GF", "YT", "PM", "BL", "MF", "NC", "PF", "WF"},
}


def read_list(path):
    if not path.exists():
        return []
    items = []
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            items.append(line)
    return items


def ripestat(call, asn):
    last_err = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(RIPESTAT.format(call=call, asn=asn), timeout=90) as r:
                data = json.load(r)
            if data.get("status") != "ok":
                raise RuntimeError(f"status={data.get('status')}")
            return data["data"]
        except Exception as e:  # netwerkfout of rate limit: even wachten
            last_err = e
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"AS{asn} {call}: ophalen mislukt: {last_err}")


def foreign_prefixes(asn, cc):
    """Prefixes waarvan geen enkele geolocatie in het land ligt (MaxMind GeoLite)."""
    ok = {cc} | EXTRA_CODES.get(cc, set())
    try:
        geo = ripestat("maxmind-geo-lite-announced-by-as", asn)
    except RuntimeError:
        return None
    out = {}
    for res in geo.get("located_resources", []):
        countries = {loc.get("country") for loc in res.get("locations", []) if loc.get("country")}
        if countries and not (countries & ok):
            out[res["resource"]] = sorted(countries)
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit("Gebruik: update_ip_list.py <landcode>")
    cc = sys.argv[1].lower()
    asns_file = ROOT / f"asns-{cc}.txt"
    exclude_file = ROOT / f"exclude-{cc}.txt"
    out_file = ROOT / f"ip-list-{cc}.txt"
    report_file = ROOT / "reports" / f"{cc}.md"

    asns = [a.upper().removeprefix("AS") for a in read_list(asns_file)]
    exclude = {ipaddress.ip_network(p) for p in read_list(exclude_file)}

    prefixes = set()
    rows, foreign_all, warnings = [], {}, []
    for asn in asns:
        holder = ripestat("as-overview", asn).get("holder", "?")
        nets = {ipaddress.ip_network(p["prefix"]) for p in ripestat("announced-prefixes", asn)["prefixes"]}
        foreign = foreign_prefixes(asn, cc.upper())
        v4 = sum(n.version == 4 for n in nets)
        n_foreign = "?" if foreign is None else len(foreign)
        rows.append(f"| AS{asn} | {holder} | {v4} | {len(nets) - v4} | {n_foreign} |")
        if not nets:
            warnings.append(f"AS{asn} ({holder}) kondigt geen prefixes aan.")
        for p, c in (foreign or {}).items():
            foreign_all[p] = (asn, c)
        print(f"AS{asn} {holder}: {len(nets)} prefixes, buitenland: {n_foreign}")
        prefixes |= nets
        time.sleep(1)

    prefixes -= exclude
    out = sorted(prefixes, key=lambda n: (n.version, n))
    v4 = sum(n.version == 4 for n in out)

    # Rapport altijd schrijven, ook als de lijst niet wordt bijgewerkt
    lines = [
        f"# Controlerapport {cc.upper()}",
        "",
        f"Gegenereerd: {datetime.datetime.now(datetime.UTC):%Y-%m-%d %H:%M} UTC. "
        f"Bron: RIPEstat. Totaal na uitsluitingen: {len(out)} prefixes ({v4} IPv4, {len(out) - v4} IPv6).",
        "",
        "| AS | Houder (RIPE) | IPv4 | IPv6 | Buiten land (GeoLite) |",
        "|---|---|---|---|---|",
        *rows,
        "",
    ]
    if warnings:
        lines += ["## Waarschuwingen", "", *[f"- {w}" for w in warnings], ""]
    still_in = {p: v for p, v in foreign_all.items() if ipaddress.ip_network(p) not in exclude}
    if still_in:
        lines += [
            "## Prefixes buiten het land die nog in de lijst staan",
            "",
            "Volgens GeoLite in gebruik buiten dit land. Voeg ze toe aan "
            f"`exclude-{cc}.txt` als ze eruit moeten.",
            "",
            *[f"- `{p}` AS{a} ({', '.join(c)})" for p, (a, c) in sorted(still_in.items())],
            "",
        ]
    report_file.parent.mkdir(exist_ok=True)
    report_file.write_text("\n".join(lines))

    if not out:
        sys.exit("Lege lijst - afgebroken.")
    if out_file.exists():
        old = [l for l in out_file.read_text().splitlines() if l.strip()]
        if len(out) < 0.8 * len(old):
            sys.exit(f"Nieuwe lijst ({len(out)}) is >20% kleiner dan de oude ({len(old)}) - afgebroken.")

    out_file.write_text("\n".join(str(n) for n in out) + "\n")
    print(f"Totaal: {len(out)} prefixes ({v4} IPv4, {len(out) - v4} IPv6)")


if __name__ == "__main__":
    main()
