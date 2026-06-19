from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DATA_CLIENT, DOMAIN
from .entity import FroehlingPe1Entity, wire_dynamic_entities


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
    wire_dynamic_entities(
        hass,
        async_add_entities,
        client,
        {"sensor", "number"},
        FroehlingPe1Sensor,
    )


class FroehlingPe1Sensor(FroehlingPe1Entity, SensorEntity):
    @property
    def native_value(self) -> Any:
        value = self._state.get("value")
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                return value
        return value

    @property
    def native_unit_of_measurement(self) -> str | None:
        return self._state.get("uom")

    @property
    def state_class(self) -> SensorStateClass | None:
        unit = self.native_unit_of_measurement
        if unit in {"°C", "%", "h", "kg", "t"}:
            return SensorStateClass.MEASUREMENT
        return None
