# ESP32 setup: from Lambdatronic to Home Assistant

This guide describes how the ESP32-WROOM reads data from the froehling PE1/Lambdatronic 3200 and sends it to Home Assistant.

## Target architecture

```text
froehling PE1 / Lambdatronic 3200
        COM2 / RS232 / Modbus RTU
                  │
                  ▼
        MAX3232 RS232-to-TTL converter
                  │
                  ▼
        ESP32-WROOM with ESPHome
                  │ Wi-Fi
                  ▼
        Home Assistant / ESPHome integration
```

The ESP32 is not a standalone server. It reads Modbus RTU values from the heater and exposes them to Home Assistant via the ESPHome API.

## 1. Prepare the ESP32

Required parts:

- AZ-Delivery ESP32-WROOM dev board
- USB cable for power and first flashing
- MAX3232 or compatible RS232-to-TTL converter
- RS232 cable to the Lambdatronic COM2 interface

Important:

- Never connect RS232 directly to ESP32 GPIO pins.
- The MAX3232 converts signal levels between RS232 and TTL.

## 2. Wiring

Default wiring used by this repository:

| ESP32-WROOM | MAX3232 TTL side |
|---|---|
| GPIO17 TX | RX |
| GPIO16 RX | TX |
| GND | GND |
| 3V3 or 5V depending on module | VCC |

The RS232 side of the MAX3232 is connected to COM2 on the Lambdatronic.

If no data arrives later:

1. Check logs.
2. Swap TX/RX on the TTL side.
3. Check the RS232 cable, because some cables/adapters require crossed lines.

## 3. Configure the Lambdatronic

COM2 on the froehling PE1/Lambdatronic 3200 must be enabled for Modbus.

Typical settings:

- Enable Modbus RTU
- Enable Modbus protocol 2014
- Use COM2 as Modbus interface
- Slave address: `2`
- Baud rate: `57600`
- Data bits: `8`
- Stop bits: `1`
- Parity: `None`

The exact menu path may differ depending on firmware.

## 4. Set ESPHome secrets

These ESPHome secrets are required:

```yaml
wifi_ssid: "YOUR_WIFI"
wifi_password: "YOUR_WIFI_PASSWORD"
froehling_api_key: "YOUR_ESPHOME_API_KEY"
froehling_ota_password: "YOUR_OTA_PASSWORD"
froehling_fallback_password: "YOUR_FALLBACK_AP_PASSWORD"
```

Do not write passwords to this GitHub repository.

## 5. Choose the ESPHome configuration

German, using the no-umlaut/no-special-character prefix:

```text
esphome/de/froehling-pe1-de.yaml
```

English, using the no-umlaut/no-special-character prefix:

```text
esphome/en/froehling-pe1-en.yaml
```

Both variants use `froehling PE1` as the device/entity base so Home Assistant creates entity IDs starting with `froehling_pe1_...`.

## 6. Flash the ESP32

Recommended process:

1. Connect ESP32 via USB.
2. Create a new ESPHome device or import the YAML file.
3. Check secrets.
4. Choose `Install` → `Plug into this computer` or local USB flashing.
5. After the first flash, connect the ESP32 to the heater.
6. Open logs.

Expected logs:

- Wi-Fi connects.
- ESPHome API starts.
- Modbus controller starts.
- No permanent Modbus timeouts.

## 7. Connect Home Assistant

When the ESP32 is online:

1. Home Assistant usually discovers the ESPHome device automatically.
2. If not: Settings → Devices & services → Add integration → ESPHome.
3. Enter the ESP32 IP address.
4. Use the API key from ESPHome secrets.
5. Verify entities.

Expected entity IDs start with:

```text
sensor.froehling_pe1_...
binary_sensor.froehling_pe1_...
select.froehling_pe1_...
number.froehling_pe1_...
```

## 8. First functional check

Read and validate values first:

- `sensor.froehling_pe1_kesseltemperatur`
- `sensor.froehling_pe1_aussentemperatur`
- `sensor.froehling_pe1_hk1_vorlauf_ist`
- `sensor.froehling_pe1_puffer_temperatur_oben`
- `sensor.froehling_pe1_pelletfuellstand`
- `sensor.froehling_pe1_anlagenzustand`
- `sensor.froehling_pe1_kesselzustand`

If temperatures are unrealistic:

- Check scaling, usually factor `0.5`.
- Check the register address.
- Check Lambdatronic Modbus settings.

## 9. Add the dashboard

After verifying entities:

1. Open `homeassistant/en/dashboard.yaml`.
2. Create a new dashboard in Home Assistant.
3. Open YAML/raw editor.
4. Paste the content.
5. Adjust missing entity IDs to the real Home Assistant entities.

## 10. Test controls only afterward

Write-capable entities are prepared but should only be tested after monitoring works.

Examples:

- `select.froehling_pe1_hc1_heating_mode`
- `number.froehling_pe1_hc1_flow_at_minus_10c_outside_temperature`
- `number.froehling_pe1_hc1_flow_at_plus_10c_outside_temperature`

Before writing:

- Is the current value read correctly?
- Does it match the heater display?
- Is the register range confirmed for your PE1/firmware?

## Problem: ESP32 online, but no values

Possible causes:

- TX/RX swapped
- wrong RS232 cable
- COM2 not enabled for Modbus
- wrong slave address
- wrong baud rate
- MAX3232 powered incorrectly
- missing GND

## Problem: values work, but dashboard shows errors

Possible causes:

- Home Assistant generated different entity IDs.
- The dashboard file needs adjustment.
- German and English variants were mixed.

Search for `froehling_pe1` in Home Assistant under Developer Tools → States and update the dashboard entity IDs accordingly.
