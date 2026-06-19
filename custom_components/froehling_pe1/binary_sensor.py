from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
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
        {"binary_sensor"},
        FroehlingPe1BinarySensor,
    )


class FroehlingPe1BinarySensor(FroehlingPe1Entity, BinarySensorEntity):
    @property
    def is_on(self) -> bool | None:
        value = self._state.get("value")
        if isinstance(value, bool):
            return value
        state = str(self._state.get("state", "")).lower()
        if state in {"on", "true", "1"}:
            return True
        if state in {"off", "false", "0"}:
            return False
        return None
