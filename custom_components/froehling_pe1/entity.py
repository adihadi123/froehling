from __future__ import annotations

from typing import Any

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .client import FroehlingPe1WebClient


class FroehlingPe1Entity(Entity):
    """Base entity mirrored from the ESPHome web_server event stream."""

    _attr_has_entity_name = False

    def __init__(self, client: FroehlingPe1WebClient, state: dict[str, Any]) -> None:
        self.client = client
        self._state = state
        self._key = str(state.get("id") or state.get("name_id") or state.get("name"))
        self._attr_unique_id = f"{client.host}_{client.port}_{self._key}"
        self._attr_name = state.get("name") or self._key

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers=self.client.device_identifiers,
            name=self.client.device.title or self.client.device.name,
            manufacturer="Fröling / ESPHome",
            model="PE1 Lambdatronic 3200 Web Server",
            configuration_url=f"http://{self.client.host}:{self.client.port}/",
        )

    @property
    def icon(self) -> str | None:
        return self._state.get("icon") or None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        attrs: dict[str, Any] = {
            "source": "ESPHome web_server /events",
            "esphome_id": self._key,
        }
        if self.client.device.uptime is not None:
            attrs["device_uptime_seconds"] = self.client.device.uptime
        return attrs

    def update_from_event(self, state: dict[str, Any]) -> None:
        self._state = state
        self.async_write_ha_state()


def wire_dynamic_entities(
    hass: HomeAssistant,
    async_add_entities: AddEntitiesCallback,
    client: FroehlingPe1WebClient,
    domain_filter: set[str],
    entity_factory,
) -> None:
    entities: dict[str, FroehlingPe1Entity] = {}

    def _handle_state(state: dict[str, Any]) -> None:
        if state.get("domain") not in domain_filter:
            return
        key = str(state.get("id") or state.get("name_id") or state.get("name"))
        if key in entities:
            entities[key].update_from_event(state)
            return
        entity = entity_factory(client, state)
        entities[key] = entity
        async_add_entities([entity])

    unsub_client = client.subscribe(_handle_state)
    hass.bus.async_listen_once("homeassistant_stop", lambda _event: unsub_client())
