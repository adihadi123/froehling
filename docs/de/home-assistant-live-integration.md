# Live-Einrichtung in Home Assistant

Diese Datei dokumentiert Roys aktuell verifizierten Live-Stand der Fröling-PE1-Anbindung in Home Assistant.

## Ergebnis

Die Fröling PE1 ist über die offizielle Home-Assistant-ESPHome-Integration eingebunden.

- ESPHome-Gerät: `froehling PE1`
- ESPHome-Node/IP: `192.168.178.192`
- ESPHome-Hostname: `esp-froehling-pe1-de.fritz.box`
- Home-Assistant-Config-Entry-Domain: `esphome`
- Home-Assistant-Config-Entry-Titel: `froehling PE1`
- Home-Assistant-Config-Entry-ID: `01KVJAWSJBWXF71CBP5FZSWDY6`
- Status bei Einrichtung: `loaded`

Geprüfte Ports am ESP:

```text
80/tcp   ESPHome web_server
6053/tcp ESPHome Native API
3232/tcp ESPHome OTA
```

## Wichtig zu Secrets

Der ESPHome Native API Encryption Key stammt aus Home Assistant:

```text
/config/esphome/secrets.yaml
froehling_api_key
```

Der Key darf nicht ins Repository geschrieben und nicht in Chat-/Log-Ausgaben ausgegeben werden.

## Live-Entity-Prefix

Durch die Kombination aus ESPHome-Gerätename und Sensorname erzeugt Home Assistant aktuell Entity-IDs mit doppeltem Prefix:

```text
froehling_pe1_froehling_pe1_...
```

Beispiele:

```text
sensor.froehling_pe1_froehling_pe1_kesseltemperatur
sensor.froehling_pe1_froehling_pe1_aussentemperatur
sensor.froehling_pe1_froehling_pe1_ruecklauftemperatur
sensor.froehling_pe1_froehling_pe1_pelletfuellstand
sensor.froehling_pe1_froehling_pe1_hk1_vorlauf_ist
sensor.froehling_pe1_froehling_pe1_hk1_vorlauf_soll
sensor.froehling_pe1_froehling_pe1_puffer_temperatur_oben
sensor.froehling_pe1_froehling_pe1_puffer_temperatur_mitte
sensor.froehling_pe1_froehling_pe1_puffer_temperatur_unten
sensor.froehling_pe1_froehling_pe1_puffer_ladezustand
sensor.froehling_pe1_froehling_pe1_pufferpumpe_ansteuerung
sensor.froehling_pe1_froehling_pe1_anlagenzustand
sensor.froehling_pe1_froehling_pe1_kesselzustand
binary_sensor.froehling_pe1_froehling_pe1_hk1_pumpe
```

Das Dashboard `homeassistant/de/dashboard.yaml` ist auf diese live verifizierten Entity-IDs angepasst.

## Beispielwerte bei Einrichtung

Bei der Live-Prüfung kamen diese Werte an:

```text
Kesseltemperatur: 53.0 °C
Pelletfüllstand: 85.714973449707 %
Puffer Ladezustand: 58.0 %
Puffer Temperatur Mitte: 127.5 °C
Anlagenzustand: Automatik
Kesselzustand: Betriebsbereit
```

Auffällig: `Puffer Temperatur Mitte` lag bei `127.5 °C`. Dieser Wert sollte gegen das reale Fröling-Display geprüft werden. Falls er dort nicht plausibel ist, muss das Register oder die Skalierung im ESPHome-Paket `puffer.yaml` überprüft werden.

## Dashboard

Live-Dashboard in Home Assistant:

- Titel: `Fröling PE1`
- URL-Pfad: `froehling-pe1`
- Modus: Storage Dashboard
- Views: Visualisierung, Kessel, Heizkreis 1, Puffer, Pellets & Austragung, Rohwerte

Repo-Vorlage:

```text
homeassistant/de/dashboard.yaml
```

Das Dashboard nutzt SVG-Bilder aus `GyroGearl00se/ESPHome-Froeling-Lambdatronic_3200` und legt Roys live verifizierte ESPHome-Entities als Lovelace-`picture-elements`-Overlays darüber. So bleibt das Dashboard ohne `custom:floorplan-card` lauffähig.

Lokale Medien im Repository:

```text
homeassistant/de/www/froeling/froeling_aio.svg
homeassistant/de/www/froeling/froeling_kessel.svg
homeassistant/de/www/froeling/froeling_heizkreis01.svg
homeassistant/de/www/froeling/froeling_puffer01.svg
homeassistant/de/www/froeling/froeling_austragung.svg
homeassistant/de/www/froeling/home.css
```

Zielpfad in Home Assistant:

```text
/config/www/froeling/
```

HTTP-Pfade in Lovelace:

```text
/local/froeling/froeling_aio.svg
/local/froeling/froeling_kessel.svg
/local/froeling/froeling_heizkreis01.svg
/local/froeling/froeling_puffer01.svg
/local/froeling/froeling_austragung.svg
```

Verifikation nach Umstellung auf die GyroGearl00se-Bilder:

```text
Dashboard vorhanden: ja
Views: 6
Entity-Referenzen: 19
Fehlende Entity-Referenzen: 0
SVG/CSS unter /local/froeling/: HTTP 200
```

## Schreib-/Steuer-Entities

Diese schreibbaren Entities existieren live:

```text
select.froehling_pe1_froehling_pe1_hk1_betriebsart
number.froehling_pe1_froehling_pe1_hk1_vorlauf_bei_minus_10c_aussentemperatur
number.froehling_pe1_froehling_pe1_hk1_vorlauf_bei_plus_10c_aussentemperatur
switch.froehling_pe1_froehling_pe1_esp_neustart
```

Sie sind bewusst nicht als Bedienelemente im Dashboard eingebaut. Schreibzugriffe auf Heizungsparameter erst freigeben, wenn Register, Wertebereiche und reales Anlagenverhalten geprüft sind.

## Custom-Integration-Fallback

Das Repository enthält weiterhin eine read-only Custom Integration unter:

```text
custom_components/froehling_pe1/
```

Diese liest `http://192.168.178.192/events` aus. Sie ist nur noch Fallback, falls die offizielle ESPHome-Integration nicht nutzbar ist oder der API-Key nicht verfügbar ist.

Für Roys aktuellen Live-Stand ist die offizielle ESPHome-Integration die bevorzugte Variante.
