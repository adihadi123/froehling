# Fröling PE1 Web custom integration

Diese Home-Assistant-Custom-Integration liest Roys ESPHome-Webserver unter `http://192.168.178.192/events` lokal und read-only aus.

Warum diese Variante?

- Der ESP ist im Netz erreichbar.
- Port `80/tcp` liefert den ESPHome-Webserver mit Server-Sent Events.
- Port `6053/tcp` ist die verschlüsselte ESPHome Native API und benötigt den echten ESPHome-API-Key.
- Solange dieser API-Key nicht sicher in Home Assistant hinterlegt ist, kann Home Assistant die offizielle ESPHome-Integration nicht abschließen.
- Die Webserver-Events liefern aber bereits die Live-Werte, ohne Schreibzugriffe auf die Heizung zu aktivieren.

## Funktionen

- lokale Push-Aktualisierung über ESPHome `/events`
- keine Cloud
- keine Passwörter im Repository
- read-only: keine Heizungsparameter werden geschrieben
- unterstützt aktuell:
  - `sensor`-Events
  - `number`-Events als read-only Sensoren
  - `binary_sensor`-Events
  - `text_sensor`-Events als Sensoren

## Installation manuell

1. Ordner kopieren:

   ```text
   custom_components/froehling_pe1
   ```

   nach:

   ```text
   /config/custom_components/froehling_pe1
   ```

2. Home Assistant neu starten.

3. Integration hinzufügen:

   ```text
   Einstellungen -> Geräte & Dienste -> Integration hinzufügen -> Fröling PE1 Web
   ```

4. Werte eintragen:

   ```text
   Host: 192.168.178.192
   Port: 80
   Name: Fröling PE1
   ```

## HACS custom repository

Wenn das Repository in HACS als benutzerdefiniertes Repository eingetragen wird:

```text
https://github.com/adihadi123/froehling
Kategorie: Integration
```

Danach Integration installieren, Home Assistant neu starten und über die UI hinzufügen.

## Sicherheit

Diese Integration nutzt bewusst nur den read-only Eventstream des ESPHome-Webservers. Schreibbare ESPHome-Entitäten wie Restart-Switches oder Heizkurven-Number-Entities werden nicht als schreibbare Home-Assistant-Controls angelegt.

Wenn später die offizielle ESPHome-Integration genutzt werden soll, muss der echte `froehling_api_key` aus der ESPHome-Konfiguration sicher in Home Assistant eingegeben werden. Der Key gehört nicht ins GitHub-Repository.
