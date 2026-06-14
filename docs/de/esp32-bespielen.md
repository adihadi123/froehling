# ESP32 mit ESPHome bespielen

Diese Anleitung beschreibt nur den Flash-/Bespiel-Weg für den ESP32-WROOM. Danach kann der ESP32 per Modbus RTU Daten von der Lambdatronic lesen und per WLAN an Home Assistant senden.

## Kurzfassung

Du brauchst:

- Home Assistant mit ESPHome Add-on oder ESPHome auf deinem PC
- ESP32-WROOM per USB am Rechner
- Datei `esphome/de/froehling-pe1-de.yaml`
- Ordner `esphome/de/packages/`
- WLAN- und ESPHome-Secrets

Der ESP32 wird nicht mit Arduino-Code bespielt, sondern mit ESPHome-YAML.

## Variante A: Über Home Assistant / ESPHome Add-on

Das ist der einfachste Weg.

### 1. Dateien ins ESPHome-Verzeichnis kopieren

In Home Assistant liegen ESPHome-Dateien normalerweise unter:

```text
/config/esphome/
```

Kopiere aus diesem Repo:

```text
esphome/de/froehling-pe1-de.yaml
esphome/de/packages/
```

nach Home Assistant:

```text
/config/esphome/froehling-pe1-de.yaml
/config/esphome/packages/base.yaml
/config/esphome/packages/kessel.yaml
/config/esphome/packages/pelletspeicher.yaml
/config/esphome/packages/heizkreis_1.yaml
/config/esphome/packages/puffer.yaml
/config/esphome/packages/steuerung.yaml
```

Wichtig: Die `packages` müssen relativ neben der Hauptdatei liegen, weil die Hauptdatei diese Includes nutzt:

```yaml
packages:
  base: !include packages/base.yaml
  kessel: !include packages/kessel.yaml
  pelletspeicher: !include packages/pelletspeicher.yaml
  heizkreis_1: !include packages/heizkreis_1.yaml
  puffer: !include packages/puffer.yaml
  steuerung: !include packages/steuerung.yaml
```

### 2. Secrets in ESPHome eintragen

Im ESPHome Add-on gibt es eine `secrets.yaml`. Dort eintragen:

```yaml
wifi_ssid: "DEIN_WLAN_NAME"
wifi_password: "DEIN_WLAN_PASSWORT"
froehling_api_key: "DEIN_ESPHOME_API_KEY"
froehling_ota_password: "DEIN_OTA_PASSWORT"
froehling_fallback_password: "DEIN_FALLBACK_AP_PASSWORT"
```

Hinweise:

- `froehling_api_key`: kann ESPHome beim Geräte-Anlegen generieren.
- `froehling_ota_password`: frei vergeben, für spätere Updates über WLAN.
- `froehling_fallback_password`: frei vergeben, für den Notfall-WLAN-Hotspot des ESP32.
- Passwörter niemals ins GitHub-Repo schreiben.

### 3. ESPHome Add-on öffnen

In Home Assistant:

```text
Einstellungen → Add-ons → ESPHome → Web UI öffnen
```

Wenn die Datei korrekt unter `/config/esphome/` liegt, sollte das Gerät `froehling-pe1-de` in ESPHome auftauchen.

Falls es nicht auftaucht:

- ESPHome Add-on neu starten.
- Dateiname prüfen: `froehling-pe1-de.yaml`
- Einrückungen/YAML prüfen.

### 4. ESP32 per USB anschließen

ESP32-WROOM per USB an den Rechner anschließen, auf dem du den Browser geöffnet hast.

Beim ersten Flashen ist USB am zuverlässigsten. OTA über WLAN geht erst nach dem ersten erfolgreichen Flash.

### 5. Installation starten

In ESPHome beim Gerät `froehling-pe1-de`:

```text
Install → Plug into this computer
```

Dann den Anweisungen im Browser folgen.

Falls der Browser seriellen Zugriff anbietet, den richtigen COM-/USB-Port auswählen.

Typische Port-Namen:

- Windows: `COM3`, `COM4`, ...
- Linux: `/dev/ttyUSB0` oder `/dev/ttyACM0`
- macOS: `/dev/tty.usbserial...`

### 6. Wenn USB-Flash aus dem Browser nicht geht

Manche Browser/Setups können nicht direkt seriell flashen. Dann im ESPHome Add-on:

```text
Install → Manual download
```

Dann wird eine Firmware-Datei erzeugt. Diese kannst du mit ESPHome Web flashen:

```text
https://web.esphome.io/
```

Ablauf:

1. ESP32 per USB anschließen.
2. Chrome/Edge öffnen.
3. `https://web.esphome.io/` öffnen.
4. `Connect` klicken.
5. Seriellen Port wählen.
6. Firmware-Datei auswählen.
7. Flash starten.

### 7. Boot-/Flash-Modus falls nötig

Viele ESP32-Devboards gehen automatisch in den Flashmodus. Falls nicht:

1. `BOOT`-Taste gedrückt halten.
2. Flash-Vorgang starten.
3. Wenn der Flash beginnt, `BOOT` loslassen.
4. Nach dem Flash ggf. `EN`/`RESET` drücken.

Wenn der Flash hängt bei `Connecting...`, ist fast immer der Bootmodus das Problem.

### 8. Logs prüfen

Nach dem Flashen in ESPHome:

```text
Logs
```

Du willst sehen:

- ESP32 startet.
- WLAN verbindet sich.
- IP-Adresse wird angezeigt.
- ESPHome API startet.
- Modbus Controller startet.

Beispiel, sinngemäß:

```text
WiFi connected
IP Address: 192.168.178.xxx
API Server started
Modbus Controller initialized
```

Modbus-Fehler sind am Anfang normal, wenn der ESP32 noch nicht mit der Heizung verbunden ist.

### 9. ESP32 an die Heizung anschließen

Nach erfolgreichem Flash:

1. ESP32 stromlos machen.
2. MAX3232 anschließen.
3. MAX3232 RS232-Seite an COM2 der Lambdatronic anschließen.
4. ESP32 wieder einschalten.
5. Logs erneut öffnen.

Verdrahtung TTL-Seite:

```text
ESP32 GPIO17 TX  -> MAX3232 RX
ESP32 GPIO16 RX  -> MAX3232 TX
ESP32 GND        -> MAX3232 GND
ESP32 3V3/5V     -> MAX3232 VCC, je nach Modul
```

### 10. Home Assistant ESPHome Integration

Wenn der ESP32 online ist:

```text
Einstellungen → Geräte & Dienste → ESPHome
```

Home Assistant erkennt das Gerät oft automatisch.

Falls nicht:

```text
Integration hinzufügen → ESPHome → IP-Adresse des ESP32 eintragen
```

Dann den API-Key verwenden, den du in `froehling_api_key` eingetragen hast.

### 11. Erste Entities prüfen

In Home Assistant:

```text
Entwicklerwerkzeuge → Zustände
```

Nach `froehling_pe1` suchen.

Erwartete Entities:

```text
sensor.froehling_pe1_kesseltemperatur
sensor.froehling_pe1_aussentemperatur
sensor.froehling_pe1_hk1_vorlauf_ist
sensor.froehling_pe1_puffer_temperatur_oben
sensor.froehling_pe1_pelletfuellstand
sensor.froehling_pe1_anlagenzustand
sensor.froehling_pe1_kesselzustand
```

## Variante B: Lokal mit ESPHome CLI

Falls du ESPHome lokal auf einem Linux-PC nutzen willst:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install esphome
```

Dann Repo/Dateien vorbereiten und flashen:

```bash
cd froehling/esphome/de
esphome run froehling-pe1-de.yaml
```

Beim ersten Flashen den seriellen Port auswählen, z.B.:

```bash
esphome run froehling-pe1-de.yaml --device /dev/ttyUSB0
```

Nach dem ersten Flash kann OTA funktionieren:

```bash
esphome run froehling-pe1-de.yaml --device froehling-pe1-de.local
```

## Häufige Fehler beim Bespielen

### Fehler: ESP32 wird nicht erkannt

Mögliche Ursachen:

- USB-Kabel ist nur Ladekabel, kein Datenkabel.
- Treiber fehlt, z.B. CP210x oder CH340.
- Falscher USB-Port.
- Browser hat keinen seriellen Zugriff.

### Fehler: Flash bleibt bei `Connecting...` hängen

Lösung:

- `BOOT` gedrückt halten, Flash starten, dann loslassen.
- Anderes USB-Kabel testen.
- Anderen USB-Port testen.

### Fehler: WLAN verbindet nicht

Prüfen:

- `wifi_ssid` korrekt?
- `wifi_password` korrekt?
- 2,4-GHz-WLAN aktiv? Viele ESP32 können kein 5 GHz.
- Empfang am Heizungsstandort ausreichend?

### Fehler: ESP32 online, aber keine Heizungswerte

Dann ist das Flashen erfolgreich, aber Modbus noch nicht:

- TX/RX tauschen.
- COM2 in Lambdatronic prüfen.
- Slave-Adresse `2` prüfen.
- Baudrate `57600` prüfen.
- RS232-Kabel prüfen.
- MAX3232-Versorgung prüfen.
- GND prüfen.

## Wichtig zur Steuerung

Nach dem Flashen erstmal nur Werte lesen.

Schreibende Entities wie `select.froehling_pe1_hk1_betriebsart` erst benutzen, wenn die gelesenen Werte plausibel sind und die Register für deine Anlage bestätigt wurden.
