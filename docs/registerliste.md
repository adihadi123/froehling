# Registerliste / Register list

Hinweis: Home Assistant Modbus nutzt Offset-Adressen. Beispiel: Register 30001 wird als Adresse 0 konfiguriert.

| Adresse | Deutsch | English | Typ | Einheit | Skalierung |
|---:|---|---|---|---|---|
| 0 | Kesseltemperatur | Furnace/boiler temperature | read/input | °C | 0.5 |
| 9 | Rücklauffühler | Return flow temperature | read/input | °C | 0.5 |
| 20 | Betriebsstunden | Operating hours | read/input | h | 1 |
| 21 | Pelletfüllstand | Pellet fill level | read/input | % | 0.0048309 ESPHome / 0.005 HA |
| 55 | Stunden seit letzter Wartung | Hours since last maintenance | read/input | h | 1 |
| 81 | Resetierbarer kg-Zähler | Resettable kg counter | read/input | kg | 1 |
| 83 | Pelletverbrauch gesamt | Total pellet consumption | read/input | t | 0.1 |
| 86 | Stunden bis Asche leeren | Hours until ash removal | read/input | h | 1 |
| 1000 | Außentemperatur | Outside temperature | read/input | °C | 0.5 |
| 1030 | HK1 Vorlauf Ist | HC1 flow actual | read/input | °C | 0.5 |
| 1031 | HK1 Vorlauf Soll | HC1 flow target | read/input | °C | 0.5 |
| 2000 | Puffer Temperatur oben | Buffer temperature top | read/input | °C | 0.5 |
| 2001 | Puffer Temperatur Mitte | Buffer temperature middle | read/input | °C | 0.5 |
| 2002 | Puffer Temperatur unten | Buffer temperature bottom | read/input | °C | 0.5 |
| 2003 | Pufferpumpen-Ansteuerung | Buffer pump control | read/input | % | 1 |
| 2006 | Puffer Ladezustand | Buffer charge | read/input | % | 1 |
| 4000 | Anlagenzustand | System status | read/input enum |  | mapping |
| 4001 | Kesselzustand | Furnace status | read/input enum |  | mapping |
| 8046 | HK1 Betriebsart | HC1 heating mode | holding/write enum |  | 0-5 |
