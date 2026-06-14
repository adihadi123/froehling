# Offene Aufgaben bis zur fertigen Home-Assistant-Integration

Diese Liste beschreibt, was noch erledigt werden muss, damit aus diesem Repository eine lauffähige Fröling-PE1-Integration für Home Assistant wird.

## 1. Hardware aufbauen

Ziel: ESP32-WROOM von AZ-Delivery über RS232/TTL mit der Lambdatronic 3200 verbinden.

Zu erledigen:

- ESP32-WROOM vorbereiten.
- MAX3232 oder kompatiblen RS232/TTL-Pegelwandler verwenden.
- GPIO17 als TX und GPIO16 als RX verwenden, falls die Beispielkonfiguration unverändert bleibt.
- GND gemeinsam verbinden.
- RS232-Seite des Wandlers mit COM2 der Lambdatronic verbinden.
- Prüfen, ob TX/RX gekreuzt werden müssen. Wenn keine Daten kommen, zuerst TX/RX tauschen.

Wichtig:

- ESP32 niemals direkt an RS232 anschließen.
- Vor dem festen Einbau erst lose testen.

## 2. Lambdatronic 3200 einstellen

Ziel: COM2 der Fröling-Steuerung als Modbus-Schnittstelle aktivieren.

Zu erledigen:

- Service-/Benutzerebene öffnen.
- Modbus RTU aktivieren.
- Modbus-Protokoll 2014 aktivieren.
- COM2 als Modbus-Schnittstelle aktivieren.
- Slave-Adresse prüfen. Dieses Repo nutzt standardmäßig Adresse `2`.
- Baudrate prüfen. Dieses Repo nutzt standardmäßig `57600`.

## 3. ESPHome Secrets anlegen

Ziel: Die ESPHome-Datei soll ohne Klartext-Passwörter funktionieren.

Benötigte Secrets in ESPHome:

```yaml
wifi_ssid: "DEIN_WLAN"
wifi_password: "DEIN_PASSWORT"
froehling_api_key: "DEIN_ESPHOME_API_KEY"
froehling_ota_password: "DEIN_OTA_PASSWORT"
froehling_fallback_password: "DEIN_FALLBACK_AP_PASSWORT"
```

Hinweis:

- API-Key kann ESPHome generieren.
- Passwörter nicht ins GitHub-Repo schreiben.

## 4. ESPHome flashen

Ziel: Der ESP32 wird mit der passenden Konfiguration geflasht.

Deutsch:

- `esphome/de/froehling-pe1-de.yaml`

Englisch:

- `esphome/en/froehling-pe1-en.yaml`

Zu erledigen:

- Datei in ESPHome importieren oder lokal kompilieren.
- Erst per USB flashen.
- Danach OTA nur nutzen, wenn das Gerät stabil im WLAN ist.
- Logs prüfen.

Erwartete erste Prüfung:

- Modbus-Kommunikation ohne Timeout.
- Außentemperatur plausibel.
- Kesseltemperatur plausibel.
- Anlagenzustand/Kesselzustand lesbar.

## 5. Register gegen deine echte Anlage prüfen

Ziel: Sicherstellen, dass die Adressen zur PE1 und deiner Lambdatronic-Version passen.

Zu prüfen:

- Kesseltemperatur: Adresse `0`
- Außentemperatur: Adresse `1000`
- HK1 Vorlauf Ist: Adresse `1030`
- HK1 Vorlauf Soll: Adresse `1031`
- Puffer oben/mitte/unten: `2000`, `2001`, `2002`
- Puffer Ladezustand: `2006`
- Pelletfüllstand: `21`
- Anlagenzustand/Kesselzustand: `4000`, `4001`

Wenn ein Wert unsinnig ist:

- Skalierung prüfen.
- Registeradresse prüfen.
- Firmware-/Anlagendokumentation vergleichen.
- Wert zunächst aus dem Dashboard entfernen oder als experimentell markieren.

## 6. Schreibzugriffe vorsichtig aktivieren

Ziel: Steuerung ermöglichen, aber nicht versehentlich falsche Heizungswerte schreiben.

Vorbereitet ist:

- HK1 Betriebsart über Register `8046`
- HK1 Heizkurvenwerte bei -10 °C und +10 °C Außentemperatur

Zu erledigen:

- Erst nur Monitoring testen.
- Dann Steuer-Entities einzeln prüfen.
- Einen ungefährlichen Zustand testen, z.B. Betriebsart lesen und mit aktuellem Display vergleichen.
- Schreibzugriffe nur durchführen, wenn Register und Wertbereich eindeutig passen.

Wichtig:

- Schreibregister können reale Heizungsparameter verändern.
- Für Automationen später zusätzliche Sperren einbauen, z.B. nur manuell, nur bei Anwesenheit, nur mit Bestätigung.

## 7. Home-Assistant-Dashboard einrichten

Ziel: Die Werte übersichtlich in Home Assistant anzeigen.

Dashboard-Dateien:

- Deutsch: `homeassistant/de/dashboard.yaml`
- Englisch: `homeassistant/en/dashboard.yaml`

Variante A: Manuelles YAML-Dashboard

1. Home Assistant öffnen.
2. Einstellungen → Dashboards.
3. Neues Dashboard anlegen, z.B. `Fröling PE1`.
4. YAML-Modus oder Raw-Konfigurationseditor nutzen.
5. Inhalt aus `homeassistant/de/dashboard.yaml` einfügen.
6. Entity-IDs prüfen und anpassen.

Variante B: Erst als Vorlage nutzen

1. Dashboard-Datei öffnen.
2. Karten einzeln in ein bestehendes Dashboard kopieren.
3. Fehlende Entities entfernen oder umbenennen.

Hinweis:

- Das Dashboard nutzt bewusst Standard-Lovelace-Karten, damit keine HACS-Abhängigkeit nötig ist.
- Später kann eine schönere Visualisierung mit `apexcharts-card`, `plotly-graph-card` oder einer Power-Flow-Karte ergänzt werden.

## 8. Optional: Modbus-TCP-Variante vorbereiten

Nur nötig, wenn statt ESPHome ein serielles Ethernet-Gateway genutzt werden soll.

Zu erledigen:

- Gateway-IP fest vergeben.
- `homeassistant/de/modbus.yaml` Host `192.168.178.xxx` anpassen.
- `configuration.yaml` ergänzen:

```yaml
modbus: !include homeassistant/de/modbus.yaml
template: !include homeassistant/de/template.yaml
```

Danach Home Assistant neu starten oder YAML-Konfiguration neu laden.

## 9. Später sinnvolle Erweiterungen

Mögliche nächste Schritte:

- Dashboard optisch schöner machen, z.B. Kessel/Puffer/Pellet-Fluss als Grafik.
- Automationen für Warnungen:
  - Pelletfüllstand niedrig.
  - Asche entleeren bald nötig.
  - Störung/Kesselzustand Fehler.
  - Puffer kalt.
- Langzeitstatistiken für Pelletverbrauch.
- Utility-Meter für Tages-/Monatsverbrauch.
- Optional Heizkurven-Steuerung mit Sicherheitsgrenzen.
- Fotos/Schaltplan deines echten Aufbaus dokumentieren.

## 10. Abnahmeliste

Die Integration gilt als erster funktionsfähiger Stand, wenn:

- ESP32 stabil online ist.
- Home Assistant alle Basiswerte sieht.
- Kesseltemperatur, Außentemperatur, HK1 und Pufferwerte plausibel sind.
- Pelletfüllstand oder Verbrauch plausibel ist.
- Dashboard ohne fehlende Entities öffnet.
- Schreibzugriffe entweder deaktiviert oder bewusst getestet sind.
