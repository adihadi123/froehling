# Hardware: ESP32-WROOM + RS232/TTL on Lambdatronic 3200

Main hardware variant for this project.

## Goal

An AZ-Delivery ESP32-WROOM reads the Lambdatronic 3200 via COM2 using Modbus RTU and exposes the values to Home Assistant through ESPHome.

## Required parts

- ESP32-WROOM dev board, e.g. AZ-Delivery ESP32 Dev Kit
- RS232-to-TTL converter, e.g. MAX3232 module
- DB9/RS232 cable to the Fröling COM2 interface
- 5 V USB power supply for the ESP32

## Example wiring

Warning: RS232 is not TTL. Never connect the ESP32 directly to RS232. Always use a MAX3232 or compatible level converter.

| ESP32 | MAX3232 TTL side |
|---|---|
| GPIO17 TX | RX |
| GPIO16 RX | TX |
| GND | GND |
| 3V3 or 5V depending on module | VCC |

Default settings in this repository:

- TX: GPIO17
- RX: GPIO16
- Baud rate: 57600
- 8 data bits
- 1 stop bit
- Parity: None
- Modbus address/slave: 2

## Lambdatronic settings

In the Fröling menu, enable approximately:

- Open user/service level
- Enable Modbus RTU
- Enable Modbus protocol 2014
- Use COM2 as Modbus interface
- Use slave address 2 unless configured differently

## ESPHome file

German:

- `esphome/de/froehling-pe1-de.yaml`

English:

- `esphome/en/froehling-pe1-en.yaml`

## Safety

- Test read-only values first.
- Verify that temperatures are plausible after flashing.
- Use write registers only if the register addresses match your Fröling firmware and configuration.
