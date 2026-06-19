from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
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
        {"text_sensor"},
        FroehlingPe1TextSensor,
    )


class FroehlingPe1TextSensor(FroehlingPe1Entity, SensorEntity):
    @property
    def native_value(self) -> str | None:
        value = self._state.get("state", self._state.get("value"))
        return None if value is None else str(value)
