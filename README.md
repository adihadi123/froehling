# Fröling PE1 / Lambdatronic 3200 für Home Assistant

Dieses Repository ist Roys bereinigte Projektbasis für eine Fröling PE1 mit Lambdatronic 3200. Die technische Geräte-/Entity-Basis heißt bewusst `froehling PE1`, damit keine Umlaute in Home-Assistant-Entity-IDs landen.

Ziel:

- Monitoring und optionale Steuerung der Fröling PE1 in Home Assistant.
- Hauptvariante: ESP32-WROOM von AZ-Delivery mit RS232/TTL-Wandler am COM2-Port.
- Zusätzlich dokumentiert: Modbus-TCP-Variante über RS232/RS485-Ethernet-Gateway.
- Deutsch und Englisch getrennt nutzbar.

Wichtig:

- Schreibzugriffe können Heizungsparameter verändern. Erst lesen, dann bewusst aktivieren.
- Die Beispielwerte basieren auf öffentlichen MIT-lizenzierten Projekten und müssen an die eigene Anlage angepasst werden.
- Fröling/Lambdatronic-Register können je nach Firmware/Anlagenkonfiguration abweichen.

## Schnellstart Deutsch

ESPHome-Variante:

1. ESP32-WROOM mit RS232/TTL-Wandler verbinden.
2. Fröling COM2 auf Modbus RTU aktivieren.
3. Datei `esphome/de/froehling-pe1-de.yaml` in ESPHome kopieren.
4. Secrets setzen: WLAN, API-Key, OTA-Passwort.
5. Flashen und Entities in Home Assistant prüfen.

Home-Assistant-Modbus-TCP-Variante:

1. RS232/RS485-zu-Ethernet-Gateway an COM2 anschließen.
2. Fröling COM2 auf Modbus RTU/TCP-Gateway passend konfigurieren.
3. `homeassistant/de/modbus.yaml` in Home Assistant einbinden.
4. `homeassistant/de/template.yaml` einbinden.
5. Optional Automationen aus `homeassistant/de/automations/` übernehmen.

## Quick start English

ESPHome variant:

1. Connect an ESP32-WROOM with an RS232/TTL converter.
2. Enable Modbus RTU on the Fröling COM2 interface.
3. Copy `esphome/en/froehling-pe1-en.yaml` into ESPHome.
4. Configure secrets: Wi-Fi, API key, OTA password.
5. Flash and verify entities in Home Assistant.

Home Assistant Modbus TCP variant:

1. Connect an RS232/RS485-to-Ethernet gateway to COM2.
2. Configure the Fröling COM2 interface and the gateway.
3. Include `homeassistant/en/modbus.yaml` in Home Assistant.
4. Include `homeassistant/en/template.yaml`.
5. Optionally import automations from `homeassistant/en/automations/`.

## Deine Anlage / Your setup

Aktueller Zuschnitt:

- Fröling PE1
- Lambdatronic 3200
- Geräte-/Entity-Basis: `froehling PE1`
- Heizkreis 1
- Pelletspeicher / Pelletfüllstand
- am Ofen angeschlossener Pufferspeicher
- Monitoring und Steuerung vorbereitet
- ESP32-WROOM AZ-Delivery als Haupt-Hardware
- Modbus-TCP-Variante zusätzlich dokumentiert

## Struktur

```text
.
├── docs/
│   ├── de/
│   └── en/
├── esphome/
│   ├── de/
│   └── en/
├── homeassistant/
│   ├── de/
│   └── en/
├── LICENSE
├── ATTRIBUTION.md
└── PROJEKTANALYSE.md
```



## Offene Aufgaben / Open tasks

Deutsch:

- `docs/de/offene-aufgaben.md`

English:

- `docs/en/open-tasks.md`



## ESP32 bespielen / flashen

Deutsch:

- `docs/de/esp32-bespielen.md`

Diese Anleitung beschreibt den konkreten Flash-Weg über Home Assistant / ESPHome Add-on, ESPHome Web und optional ESPHome CLI.

## ESP32-Datenweg / ESP32 data flow

Deutsch:

- `docs/de/esp32-esphome-datenfluss.md`

English:

- `docs/en/esp32-esphome-data-flow.md`

Naming-Konvention: Geräte- und Entity-Basis ist bewusst `froehling PE1`, damit Home Assistant Entity-IDs mit `froehling_pe1_...` erzeugt und keine Umlaute im Prefix vorkommen.

## Home Assistant Dashboard

Dieses Repository enthält erste Lovelace-Dashboard-Vorlagen ohne HACS-Abhängigkeiten:

Deutsch:

- `homeassistant/de/dashboard.yaml`

English:

- `homeassistant/en/dashboard.yaml`

Die Dashboards sind als Startpunkt gedacht. Nach dem ersten ESPHome-Import müssen die Entity-IDs in Home Assistant geprüft und ggf. angepasst werden.

## Quellen / Attribution

Dieses Projekt fasst Ideen und Register aus diesen MIT-lizenzierten Projekten zusammen:

- `GyroGearl00se/ESPHome-Froeling-Lambdatronic_3200`
- `smokyflex/pe1-modbus`

Details stehen in `ATTRIBUTION.md`.
