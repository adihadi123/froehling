# Open tasks until the Home Assistant integration is complete

This list describes what still needs to be done to turn this repository into a working froehling PE1 integration for Home Assistant.

## 1. Build the hardware

Goal: connect an AZ-Delivery ESP32-WROOM to the Lambdatronic 3200 using RS232/TTL.

To do:

- Prepare the ESP32-WROOM.
- Use a MAX3232 or compatible RS232/TTL level converter.
- Use GPIO17 as TX and GPIO16 as RX if the example configuration remains unchanged.
- Connect common GND.
- Connect the RS232 side of the converter to COM2 on the Lambdatronic.
- Check whether TX/RX must be crossed. If no data arrives, swap TX/RX first.

Important:

- Never connect the ESP32 directly to RS232.
- Test loosely before final installation.

## 2. Configure the Lambdatronic 3200

Goal: enable COM2 as the Modbus interface.

To do:

- Open user/service level.
- Enable Modbus RTU.
- Enable Modbus protocol 2014.
- Enable COM2 as Modbus interface.
- Check the slave address. This repo uses address `2` by default.
- Check the baud rate. This repo uses `57600` by default.

## 3. Create ESPHome secrets

Goal: keep passwords out of the repository.

Required ESPHome secrets:

```yaml
wifi_ssid: "YOUR_WIFI"
wifi_password: "YOUR_PASSWORD"
froehling_api_key: "YOUR_ESPHOME_API_KEY"
froehling_ota_password: "YOUR_OTA_PASSWORD"
froehling_fallback_password: "YOUR_FALLBACK_AP_PASSWORD"
```


Detailed guide: `docs/en/esp32-esphome-data-flow.md`

## 4. Flash ESPHome

Goal: flash the ESP32 with the selected configuration.

German:

- `esphome/de/froehling-pe1-de.yaml`

English:

- `esphome/en/froehling-pe1-en.yaml`

To do:

- Import the file into ESPHome or compile locally.
- Flash via USB first.
- Use OTA only after Wi-Fi is stable.
- Check logs.

Expected first checks:

- Modbus communication without timeouts.
- Plausible outside temperature.
- Plausible boiler temperature.
- Readable system/furnace status.

## 5. Verify registers against the real system

Goal: ensure the addresses match the PE1 and Lambdatronic firmware.

Check:

- Boiler temperature: address `0`
- Outside temperature: address `1000`
- HC1 flow actual: address `1030`
- HC1 flow target: address `1031`
- Buffer top/middle/bottom: `2000`, `2001`, `2002`
- Buffer charge: `2006`
- Pellet fill level: `21`
- System/furnace status: `4000`, `4001`

If a value is wrong:

- Check scaling.
- Check the register address.
- Compare with firmware/system documentation.
- Remove it from the dashboard or mark it as experimental.

## 6. Enable write access carefully

Goal: allow control without accidentally writing wrong heating settings.

Prepared write controls:

- HC1 heating mode via register `8046`
- HC1 heating curve values at -10 °C and +10 °C outside temperature

To do:

- Test monitoring first.
- Then test control entities one by one.
- Compare the current value with the heater display.
- Only write if register and allowed value range are confirmed.

Important:

- Write registers can change real heating parameters.
- Add safety restrictions to automations later.

## 7. Set up the Home Assistant dashboard

Goal: display the values clearly in Home Assistant.

Dashboard files:

- German: `homeassistant/de/dashboard.yaml`
- English: `homeassistant/en/dashboard.yaml`

Option A: manual YAML dashboard

1. Open Home Assistant.
2. Go to Settings → Dashboards.
3. Create a new dashboard, e.g. `froehling PE1`.
4. Use YAML mode or the raw configuration editor.
5. Paste the content from `homeassistant/en/dashboard.yaml`.
6. Check and adjust entity IDs.

Option B: use as a template

1. Open the dashboard file.
2. Copy cards into an existing dashboard one by one.
3. Remove or rename missing entities.

Note:

- The dashboard intentionally uses standard Lovelace cards only.
- Later, a nicer visualization can be added with `apexcharts-card`, `plotly-graph-card`, or a power-flow card.

## 8. Optional: prepare the Modbus TCP variant

Only needed when using a serial Ethernet gateway instead of ESPHome.

To do:

- Assign a static gateway IP.
- Adjust the `192.168.178.xxx` host in `homeassistant/en/modbus.yaml`.
- Include in `configuration.yaml`:

```yaml
modbus: !include homeassistant/en/modbus.yaml
template: !include homeassistant/en/template.yaml
```

Restart Home Assistant or reload YAML configuration afterward.

## 9. Useful future extensions

Possible next steps:

- Improve dashboard visuals, e.g. boiler/buffer/pellet flow graphics.
- Add warning automations:
  - low pellet fill level,
  - ash removal due soon,
  - fault/furnace status error,
  - buffer cold.
- Add long-term pellet consumption statistics.
- Add utility meters for daily/monthly consumption.
- Optional heating curve control with safety limits.
- Document photos/wiring of the real setup.

## 10. Acceptance checklist

The first integration version is usable when:

- ESP32 is online reliably.
- Home Assistant sees all basic values.
- Boiler temperature, outside temperature, HC1 and buffer values are plausible.
- Pellet fill level or consumption is plausible.
- Dashboard opens without missing entities.
- Write access is either disabled or deliberately tested.
