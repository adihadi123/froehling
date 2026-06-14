# Projektanalyse: Fröling / Lambdatronic 3200 Integration

Stand: 2026-06-14

Verglichene Repositories:

- `adihadi123/ESPHome-Froeling-Lambdatronic_3200`
  - Fork von `GyroGearl00se/ESPHome-Froeling-Lambdatronic_3200`
  - Ansatz: ESP32/Wemos mit RS232-TTL-Adapter direkt an COM2, ESPHome liest Modbus RTU und liefert Entities direkt an Home Assistant.

- `adihadi123/pe1-modbus`
  - Fork von `smokyflex/pe1-modbus`
  - Ansatz: RS232/RS485-zu-Ethernet-Konverter, Home Assistant liest Modbus TCP direkt; optional Python/MQTT-Skripte.

Zielrepo:

- `adihadi123/froehling`
  - soll später Roys eigene, bereinigte und auf seine Anlage zugeschnittene Variante enthalten.

## Kurzfazit

Beide Projekte nutzen letztlich dieselbe Modbus-Welt der Fröling Lambdatronic 3200, unterscheiden sich aber stark im Betriebsmodell:

- ESPHome-Repo ist besser, wenn ein kleiner ESP32 als Gateway direkt an der Heizung laufen soll.
- pe1-modbus ist besser, wenn ein LAN-Modbus-Gateway oder eine direkte Modbus-TCP-Anbindung bevorzugt wird und Home Assistant die Register selbst abfragt.
- Für Roys eigenes Repo bietet sich eine saubere Kombination an:
  - Register-/Adresswissen aus beiden Repos zusammenführen.
  - Zwei Installationsvarianten dokumentieren: ESPHome/RTU und Home-Assistant-Modbus/TCP.
  - Nur die tatsächlich vorhandenen Komponenten aktivieren.
  - Eigene Entity-Namen, eigene Dashboard-Struktur und eigene README auf Deutsch.

## Technischer Vergleich

| Thema | ESPHome-Froeling-Lambdatronic_3200 | pe1-modbus | Empfehlung für eigenes Repo |
|---|---|---|---|
| Verbindung | ESP32/Wemos D1 Mini32 + MAX3232 an COM2 | Waveshare RS232/RS485 zu Ethernet, Modbus TCP | Abhängig von Roys Hardware; beide Varianten trennen |
| Home Assistant Integration | ESPHome API | HA `modbus:` Integration direkt, optional MQTT | Beide Varianten dokumentieren, aber eine Hauptvariante wählen |
| Protokoll | Modbus RTU über UART | Modbus TCP Port 502 | Gemeinsame Registerliste pflegen |
| Slave/Adresse | Modbus Controller `address: 2` | `slave: 2` | Einheitlich als Parameter dokumentieren |
| Update-Intervall | meist 60 s am ESPHome Controller | 30 s Sensoren, 3600 s Langzeitwerte | Sensorgruppen mit sinnvollen Intervallen definieren |
| Entitäten | viele deutsch benannte ESPHome Entities | englisch benannte HA Modbus Entities | Eigene Namenskonvention festlegen, bevorzugt deutsch oder konsistent englisch |
| Statusmapping | direkt in ESPHome C++ Lambda | HA Template-Sensoren | Zentrale Mapping-Datei/Template bevorzugen |
| Schreibzugriffe | ESPHome `number`/`select`/`switch` auf Holding/Coil/Register | HA `modbus.write_register` Beispiele | Schreibzugriffe vorsichtig, optional und klar gekennzeichnet |
| Dashboard | Floorplan/SVG mit vielen Dateien | Lovelace picture-elements/apexcharts/plotly Beispiele | Eigenes Dashboard schlank und modular bauen |
| Lizenz | MIT | MIT | Kombination möglich, Copyright-Hinweise beibehalten |

## Umfang der Repos

### ESPHome-Froeling-Lambdatronic_3200

Dateien/Module:

- `froeling.yaml`: Hauptdatei für ESPHome, ESP32, UART, Modbus Controller, Statussensoren und Packages.
- `kessel.yaml`: Kesselwerte, Lambda/Sauerstoff, Temperaturen, Betriebsstunden, Wartung, Asche.
- `austragung.yaml`: Pelletstand und Pelletverbrauch.
- `boiler_01.yaml`: Boiler/Brauchwasser.
- `heizkreis01.yaml`, `heizkreis02.yaml`: Heizkreise 1 und 2 inkl. Pumpen, Vorlauf, Betriebsart und Sollwerte.
- `puffer_01.yaml`: Pufferspeicher oben/mitte/unten, Pumpe, Ladezustand.
- `solarthermie.yaml`: Solarthermie-Werte.
- `zirkulationspumpe.yaml`: Zirkulationspumpe/Rücklauftemperatur.
- `ha_dashboard.yaml` und `ha_dashboard/`: Floorplan/SVG-Dashboard.
- 3D-Druck-Dateien für ESP32/RS232-Gehäuse.

Stärken:

- Sehr komplette ESPHome-Basis.
- Viele Fröling-Komponenten bereits modular getrennt.
- Statuswerte werden direkt als lesbare Textsensoren gemappt.
- Für eine autarke kleine Gateway-Hardware gut geeignet.

Schwächen/Risiken:

- ESPHome-Entity-Namen hängen stark am Gerätenamen `froeling`; Dashboard empfiehlt diesen Namen nicht zu ändern.
- Viele Komponenten sind pauschal enthalten und müssen für die eigene Anlage entfernt werden.
- Remote Packages zeigen im README noch auf das Originalrepo, nicht auf Roys Fork/eigenes Repo.
- Schreibbare Werte sind vorhanden; diese sollten für Roys Variante bewusst aktiviert/deaktiviert werden.

### pe1-modbus

Dateien/Module:

- `modbus.yaml`: Home-Assistant-Modbus-Konfiguration für TCP-Hub und Sensoren.
- `template.yaml`: Templates für Statusmappings und Visualisierungs-Helfer.
- `visualization/`: Lovelace-Beispiele für Systemstatus, Heizkurve, Buffer, Warmwasser, Verbrauch.
- `src/pe1modbus/`: optionaler Python/MQTT-Ansatz mit Registerdefinitionen.

Stärken:

- Sehr gut als Home-Assistant-native Modbus-TCP-Vorlage.
- Saubere Beispiele für Template-Sensoren und Lovelace-Visualisierung.
- Enthält Python-Registermodell, nützlich als Register-Dokumentation.
- Gute Beispiele für Remote Control per `modbus.write_register`.

Schwächen/Risiken:

- Weniger vollständig als ESPHome-Repo; ca. 27 aktive Modbus-Sensoren im `modbus.yaml`.
- README ist teilweise PE1-spezifisch und englisch.
- Beispiel-Hub heißt `pe1_test`; muss angepasst werden.
- Template-Datei sollte vor Übernahme strukturell geprüft/angepasst werden, da einige Visualisierungs-Sensoren sehr projektspezifisch sind.

## Gemeinsame Register / Überschneidungen

Diese Register kommen in beiden Projekten vor und sind gute Kandidaten für Roys Basisumfang:

| Adresse | Bedeutung |
|---:|---|
| 0 | Kesseltemperatur / Furnace Temperature |
| 9 | Rücklauffühler / Return Flow Temperature |
| 20 | Betriebsstunden |
| 21 | Pellet-Füllstand |
| 55 | Stunden seit letzter Wartung |
| 81 | Pelletverbrauch kg / resetierbarer kg-Zähler |
| 83 | Pelletverbrauch Gesamt |
| 86 | Stunden bis Asche entleeren |
| 711 | Rücklauftemperatur Zirkulationsleitung |
| 1000 | Außentemperatur |
| 1030 | Heizkreis 1 Vorlauf Ist |
| 1031 | Heizkreis 1 Vorlauf Soll |
| 1032 | Raumtemperatur / teils HK1-Sollwert je nach Kontext |
| 1630 | Boiler 1 Temperatur oben |
| 1632 | Boilerpumpe / Boiler-Nachladen-Kontext |
| 2000 | Puffer Temperatur oben |
| 2002 | Puffer Temperatur unten |
| 2003 | Pufferpumpen-Ansteuerung |
| 2006 | Puffer Ladezustand |
| 4000 | Anlagenzustand |
| 4001 | Kesselzustand |
| 8046 | Heizkreis 1 Betriebsart / Holding Register |

Hinweis: Die Adressen in Home Assistant Modbus sind bereits als Offset angegeben, z.B. 30001 -> Adresse 0, 34001 -> Adresse 4000. Das sollte im eigenen Repo klar dokumentiert werden.

## Zusätzliche ESPHome-Register, die interessant sein können

Nur oder vor allem im ESPHome-Repo aktiv enthalten:

- Abgastemperatur
- Restsauerstoffgehalt
- Saugzugdrehzahl
- Primärluft / Sekundärluft
- Sauerstoffregler
- Betriebsstunden Feuererhaltung
- Resetierbarer Tonnen-Zähler
- Pelletlager Restbestand als Holding-Wert
- Heizkreis 2 komplett
- Puffer Mitte
- Solarthermie komplett
- Zirkulationspumpen-Drehzahl und Strömungsschalter

## Vorgeschlagene Zielstruktur für `adihadi123/froehling`

```text
froehling/
├── README.md
├── LICENSE
├── docs/
│   ├── hardware-esphome-rtu.md
│   ├── hardware-modbus-tcp.md
│   ├── registerliste.md
│   └── home-assistant.md
├── esphome/
│   ├── froehling.yaml
│   └── packages/
│       ├── kessel.yaml
│       ├── pellet.yaml
│       ├── heizkreis_1.yaml
│       ├── heizkreis_2.yaml
│       ├── boiler.yaml
│       ├── puffer.yaml
│       ├── zirkulation.yaml
│       └── solarthermie.yaml
├── homeassistant/
│   ├── modbus.yaml
│   ├── template.yaml
│   ├── automations/
│   └── dashboards/
└── tools/
    └── register_export.py
```

## Empfohlene Vorgehensweise

1. Roy legt fest, welche Hardware-Variante genutzt werden soll:
   - ESP32 direkt an COM2 per RS232/TTL,
   - oder RS232/RS485-Ethernet-Gateway mit Modbus TCP,
   - oder beide Varianten im Repo behalten.

2. Roy nennt die reale Heizungsanlage und Komponenten:
   - Fröling Modell,
   - Lambdatronic-Version,
   - Heizkreise,
   - Boiler/Brauchwasser,
   - Pufferspeicher,
   - Solarthermie,
   - Zirkulationspumpe,
   - Pelletlager/Austragung.

3. Daraus wird eine minimale Registerliste gebaut:
   - Basiswerte immer aktiv,
   - optionale Komponenten modular,
   - Schreibzugriffe nur nach ausdrücklicher Entscheidung.

4. Eigenes Repo wird nicht einfach ein Fork-Dump, sondern eine aufgeräumte Roy-Version:
   - deutsche README,
   - klare Warnhinweise für Schreibregister,
   - saubere Entity-Namen,
   - keine unnötigen Dashboard-/Bilddateien,
   - MIT-Lizenz inkl. Attribution an beide Ursprungsprojekte.

## Offene Fragen an Roy

1. Welche Hardware willst du einsetzen?
   - ESP32/Wemos + MAX3232 direkt an COM2?
   - Waveshare/anderer RS232-zu-Ethernet-Konverter?
   - Etwas anderes?

2. Welche Fröling-Heizung genau?
   - Modell, z.B. PE1, SP Dual, P4, S4 usw.
   - Lambdatronic-Version, falls bekannt.

3. Welche Komponenten hast du wirklich?
   - Anzahl Heizkreise?
   - Boiler/Brauchwasser?
   - Pufferspeicher, wie viele Sensoren oben/mitte/unten?
   - Solarthermie?
   - Zirkulationspumpe?
   - Pelletlager/Füllstand?

4. Sollen wir nur lesen oder auch steuern?
   - Nur Monitoring ist sicherer.
   - Steuerung z.B. Heizmodus/Solltemperaturen nur bewusst und mit Sicherheits-Hinweisen.

5. Sprache/Namensschema:
   - Deutsche Entity-Namen wie `froehling_kesseltemperatur`?
   - Oder technisch/englisch wie `froehling_furnace_temperature`?

6. Ziel in Home Assistant:
   - Nur Entities bereitstellen?
   - Zusätzlich Dashboard?
   - Zusätzlich Automationen/Benachrichtigungen?
