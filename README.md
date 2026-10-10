# palo-alto-edl
Pasting this data from Prisma Browser is prohibited

## IP-lijsten per land

Prefixes (IPv4 en IPv6) van internetproviders met een eigen netwerk, per land.
Elke maandag automatisch bijgewerkt via RIPEstat (GitHub Action *Update IP-lijsten*).

| Land | Lijst | AS-nummers | Uitsluitingen | Controlerapport |
|---|---|---|---|---|
| Nederland | `ip-list-nl.txt` | `asns-nl.txt` | `exclude-nl.txt` | `reports/nl.md` |
| Frankrijk | `ip-list-fr.txt` | `asns-fr.txt` | `exclude-fr.txt` | `reports/fr.md` |
| Duitsland | `ip-list-de.txt` | `asns-de.txt` | `exclude-de.txt` | `reports/de.md` |
| Oostenrijk | `ip-list-at.txt` | `asns-at.txt` | `exclude-at.txt` | `reports/at.md` |
| Zwitserland | `ip-list-ch.txt` | `asns-ch.txt` | `exclude-ch.txt` | `reports/ch.md` |
| België | `ip-list-be.txt` | `asns-be.txt` | `exclude-be.txt` | `reports/be.md` |
| Luxemburg | `ip-list-lu.txt` | `asns-lu.txt` | `exclude-lu.txt` | `reports/lu.md` |
| Spanje | `ip-list-es.txt` | `asns-es.txt` | `exclude-es.txt` | `reports/es.md` |
| Italië | `ip-list-it.txt` | `asns-it.txt` | `exclude-it.txt` | `reports/it.md` |
| Portugal | `ip-list-pt.txt` | `asns-pt.txt` | `exclude-pt.txt` | `reports/pt.md` |

- **Land toevoegen:** maak `asns-<landcode>.txt` aan; de Action pakt het automatisch op.
- **Controlerapport:** per AS de houder volgens RIPE, het aantal prefixes en welke prefixes volgens GeoLite buiten het land in gebruik zijn.
- **Handmatig bijwerken:** tabblad **Actions** > *Update IP-lijsten* > **Run workflow**.
- **Veiligheidsrem:** bij een lege lijst of >20% daling wordt de lijst van dat land niet overschreven.

EDL-URL's:
- Nederland: `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-nl.txt`
- Frankrijk: `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-fr.txt`
- Duitsland: `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-de.txt`
- Oostenrijk: `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-at.txt`
- Zwitserland: `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-ch.txt`
- België: `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-be.txt`
- Luxemburg: `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-lu.txt`
- Spanje: `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-es.txt`
- Italië: `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-it.txt`
- Portugal: `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-pt.txt`
