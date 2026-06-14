# Hardware: ESP32-WROOM + RS232/TTL an Lambdatronic 3200

Hauptvariante für dieses Projekt.

## Ziel

Ein ESP32-WROOM von AZ-Delivery liest die Lambdatronic 3200 über COM2 per Modbus RTU und stellt die Werte über ESPHome in Home Assistant bereit.

## Benötigt

- ESP32-WROOM Dev Board, z.B. AZ-Delivery ESP32 Dev Kit
- RS232-zu-TTL-Wandler, z.B. MAX3232-Modul
- DB9-/RS232-Kabel zur Fröling COM2-Schnittstelle
- 5 V USB-Netzteil für den ESP32

## Verdrahtung Beispiel

Achtung: RS232 ist nicht TTL. Den ESP32 niemals direkt an RS232 anschließen. Immer MAX3232 oder kompatiblen Pegelwandler nutzen.

| ESP32 | MAX3232 TTL-Seite |
|---|---|
| GPIO17 TX | RX |
| GPIO16 RX | TX |
| GND | GND |
| 3V3 oder 5V nach Modulvorgabe | VCC |

Standard in dieser Repo-Konfiguration:

- TX: GPIO17
- RX: GPIO16
- Baudrate: 57600
- 8 Datenbits
- 1 Stoppbit
- Parität: None
- Modbus-Adresse/Slave: 2

## Lambdatronic Einstellungen

Im Fröling-Menü sinngemäß:

- Benutzer-/Serviceebene öffnen
- Modbus RTU aktivieren
- Modbus-Protokoll 2014 aktivieren
- COM2 als Modbus-Schnittstelle verwenden
- Slave-Adresse 2 verwenden, falls nicht anders konfiguriert

## ESPHome Datei

Deutsch:

- `esphome/de/froehling-pe1-de.yaml`

Englisch:

- `esphome/en/froehling-pe1-en.yaml`

## Sicherheit

- Erst ohne Schreibaktionen testen.
- Nach dem Flashen prüfen, ob die gelesenen Temperaturen plausibel sind.
- Steuerregister nur nutzen, wenn die Registeradressen zur eigenen Fröling-Version passen.
