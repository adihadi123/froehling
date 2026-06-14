# Alternative Hardware: Modbus TCP Gateway

Diese Variante ist dokumentiert, falls statt ESP32 ein RS232/RS485-zu-Ethernet-Gateway genutzt werden soll.

## Prinzip

Die Fröling COM2-Schnittstelle wird über ein serielles Ethernet-Gateway in Modbus TCP bereitgestellt. Home Assistant fragt die Register dann direkt über die `modbus:` Integration ab.

## Benötigt

- RS232/RS485-zu-Ethernet-Gateway, z.B. Waveshare Industrial RS232/RS485 to Ethernet Converter
- Passendes RS232-Kabel zur Fröling COM2-Schnittstelle
- Feste IP-Adresse für das Gateway

## Home Assistant Dateien

Deutsch:

- `homeassistant/de/modbus.yaml`
- `homeassistant/de/template.yaml`

Englisch:

- `homeassistant/en/modbus.yaml`
- `homeassistant/en/template.yaml`

## configuration.yaml Beispiel

```yaml
modbus: !include homeassistant/de/modbus.yaml
template: !include homeassistant/de/template.yaml
```

Den Host `192.168.x.x` in `modbus.yaml` an die IP des Gateways anpassen.
