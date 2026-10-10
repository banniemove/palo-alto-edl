# palo-alto-edl
Pasting this data from Prisma Browser is prohibited

## IP-lijsten per land

Prefixes (IPv4 en IPv6) van internetproviders met een eigen netwerk, per land.
Elke maandag automatisch bijgewerkt via RIPEstat (GitHub Action *Update IP-lijsten*).

| Land | Lijst | AS-nummers | Uitsluitingen |
|---|---|---|---|
| Nederland | `ip-list-nl.txt` | `asns-nl.txt` | `exclude-nl.txt` |
| Frankrijk | `ip-list-fr.txt` | `asns-fr.txt` | `exclude-fr.txt` |

- Handmatig bijwerken: tabblad **Actions** > *Update IP-lijsten (NL, FR)* > **Run workflow**
- Veiligheidsrem: bij een AS met 0 prefixes of >20% daling wordt de lijst niet overschreven.

EDL-URL's:
- `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-nl.txt`
- `https://raw.githubusercontent.com/banniemove/palo-alto-edl/refs/heads/main/ip-list-fr.txt`
