# ESP32 einrichten: Von der Lambdatronic zu Home Assistant

Diese Anleitung beschreibt den praktischen Weg, wie der ESP32-WROOM die Daten der froehling PE1/Lambdatronic 3200 liest und an Home Assistant sendet.

## Zielbild

```text
froehling PE1 / Lambdatronic 3200
        COM2 / RS232 / Modbus RTU
                  │
                  ▼
        MAX3232 RS232-zu-TTL-Wandler
                  │
                  ▼
        ESP32-WROOM mit ESPHome
                  │ WLAN
                  ▼
        Home Assistant / ESPHome Integration
```

Der ESP32 ist dabei kein eigener Server. Er liest per Modbus RTU Werte von der Heizung und meldet sie über die ESPHome-API an Home Assistant.

## 1. ESP32 vorbereiten

Benötigt:

- AZ-Delivery ESP32-WROOM Dev Board
- USB-Kabel für Strom und erstes Flashen
- MAX3232 oder kompatibler RS232-zu-TTL-Wandler
- RS232-Kabel zur COM2-Schnittstelle der Lambdatronic

Wichtig:

- RS232 darf nicht direkt an GPIO-Pins des ESP32 angeschlossen werden.
- Der MAX3232 wandelt die Pegel zwischen RS232 und TTL.

## 2. Verdrahtung

Standard in dieser Repo-Konfiguration:

| ESP32-WROOM | MAX3232 TTL-Seite |
|---|---|
| GPIO17 TX | RX |
| GPIO16 RX | TX |
| GND | GND |
| 3V3 oder 5V nach Modulvorgabe | VCC |

Die RS232-Seite des MAX3232 wird mit COM2 der Lambdatronic verbunden.

Wenn später keine Daten ankommen:

1. Logs prüfen.
2. TX/RX auf TTL-Seite tauschen.
3. RS232-Kabel prüfen, da je nach Kabel/Adapter gekreuzte Leitungen nötig sein können.

## 3. Lambdatronic einstellen

An der froehling PE1/Lambdatronic 3200 muss COM2 für Modbus aktiviert werden.

Typische Einstellungen:

- Modbus RTU aktivieren
- Modbus-Protokoll 2014 aktivieren
- COM2 als Modbus-Schnittstelle aktivieren
- Slave-Adresse: `2`
- Baudrate: `57600`
- Datenbits: `8`
- Stoppbits: `1`
- Parität: `None`

Die genaue Menüführung kann je nach Firmware abweichen.

## 4. ESPHome Secrets setzen

In ESPHome müssen diese Secrets vorhanden sein:

```yaml
wifi_ssid: "DEIN_WLAN"
wifi_password: "DEIN_WLAN_PASSWORT"
froehling_api_key: "DEIN_ESPHOME_API_KEY"
froehling_ota_password: "DEIN_OTA_PASSWORT"
froehling_fallback_password: "DEIN_FALLBACK_AP_PASSWORT"
```

Keine Passwörter in dieses GitHub-Repo schreiben.

## 5. ESPHome-Konfiguration wählen

Deutsch ohne Umlaut-/Sonderzeichen-Prefix:

```text
esphome/de/froehling-pe1-de.yaml
```

Englisch ohne Umlaut-/Sonderzeichen-Prefix:

```text
esphome/en/froehling-pe1-en.yaml
```

Beide Varianten verwenden als Geräte-/Entity-Basis `froehling PE1`, damit Home Assistant Entity-IDs mit `froehling_pe1_...` erzeugt.

Detailanleitung zum Bespielen/Flashen: `docs/de/esp32-bespielen.md`

## 6. ESP32 flashen

Empfohlener Ablauf:

1. ESP32 per USB anschließen.
2. In ESPHome ein neues Gerät anlegen oder die YAML-Datei importieren.
3. Secrets prüfen.
4. `Install` → `Plug into this computer` oder lokales USB-Flashen wählen.
5. Nach dem ersten Flashen ESP32 mit der Heizung verbinden.
6. Logs öffnen.

Erwartung in den Logs:

- WLAN verbindet sich.
- ESPHome API startet.
- Modbus Controller startet.
- Keine dauerhaften Modbus-Timeouts.

## 7. Home Assistant verbinden

Wenn der ESP32 online ist:

1. Home Assistant erkennt das ESPHome-Gerät normalerweise automatisch.
2. Falls nicht: Einstellungen → Geräte & Dienste → Integration hinzufügen → ESPHome.
3. IP-Adresse des ESP32 eintragen.
4. API-Key aus den ESPHome-Secrets verwenden.
5. Entities prüfen.

Erwartete Entity-IDs beginnen mit:

```text
sensor.froehling_pe1_...
binary_sensor.froehling_pe1_...
select.froehling_pe1_...
number.froehling_pe1_...
```

## 8. Erste Funktionsprüfung

Zuerst nur lesen und plausibilisieren:

- `sensor.froehling_pe1_kesseltemperatur`
- `sensor.froehling_pe1_aussentemperatur`
- `sensor.froehling_pe1_hk1_vorlauf_ist`
- `sensor.froehling_pe1_puffer_temperatur_oben`
- `sensor.froehling_pe1_pelletfuellstand`
- `sensor.froehling_pe1_anlagenzustand`
- `sensor.froehling_pe1_kesselzustand`

Wenn Temperaturen unrealistisch sind:

- Skalierung prüfen, meist Faktor `0.5`.
- Registeradresse prüfen.
- Modbus-Einstellung der Lambdatronic prüfen.

## 9. Dashboard einbinden

Nach erfolgreicher Entity-Prüfung:

1. Datei `homeassistant/de/dashboard.yaml` öffnen.
2. In Home Assistant ein neues Dashboard anlegen.
3. YAML/Raw-Editor öffnen.
4. Inhalt einfügen.
5. Fehlende Entity-IDs anhand der echten Home-Assistant-Entities korrigieren.

## 10. Steuerung erst danach testen

Schreibende Entitäten sind vorbereitet, sollen aber erst nach erfolgreichem Monitoring getestet werden.

Beispiele:

- `select.froehling_pe1_hk1_betriebsart`
- `number.froehling_pe1_hk1_vorlauf_bei_minus_10c_aussentemperatur`
- `number.froehling_pe1_hk1_vorlauf_bei_plus_10c_aussentemperatur`

Vor dem Schreiben prüfen:

- Wird der aktuelle Wert korrekt gelesen?
- Passt die Anzeige zur Heizung?
- Ist der Registerbereich für deine PE1/Firmware bestätigt?

## Fehlerbild: ESP32 online, aber keine Werte

Mögliche Ursachen:

- TX/RX vertauscht
- falsches RS232-Kabel
- COM2 nicht als Modbus aktiviert
- falsche Slave-Adresse
- falsche Baudrate
- MAX3232 falsch versorgt
- GND fehlt

## Fehlerbild: Werte kommen, aber Dashboard zeigt Fehler

Mögliche Ursachen:

- Home Assistant hat Entity-IDs anders erzeugt.
- Dashboard-Datei muss angepasst werden.
- Deutsche/englische Variante wurde gemischt.

Dann in Home Assistant unter Entwicklerwerkzeuge → Zustände nach `froehling_pe1` suchen und die Entity-IDs im Dashboard entsprechend korrigieren.
