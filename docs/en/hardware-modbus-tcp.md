# Alternative hardware: Modbus TCP gateway

This variant is documented in case an RS232/RS485-to-Ethernet gateway is used instead of ESP32.

## Concept

The Fröling COM2 serial interface is exposed through an Ethernet gateway. Home Assistant reads the registers directly via the `modbus:` integration.

## Required parts

- RS232/RS485-to-Ethernet gateway, e.g. Waveshare Industrial RS232/RS485 to Ethernet Converter
- Suitable RS232 cable to the Fröling COM2 interface
- Static IP address for the gateway

## Home Assistant files

German:

- `homeassistant/de/modbus.yaml`
- `homeassistant/de/template.yaml`

English:

- `homeassistant/en/modbus.yaml`
- `homeassistant/en/template.yaml`

## configuration.yaml example

```yaml
modbus: !include homeassistant/en/modbus.yaml
template: !include homeassistant/en/template.yaml
```

Adjust the `192.168.x.x` host in `modbus.yaml` to your gateway IP.
