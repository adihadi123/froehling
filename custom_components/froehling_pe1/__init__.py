from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .client import FroehlingPe1WebClient
from .const import CONF_HOST, CONF_NAME, CONF_PORT, DATA_CLIENT, DEFAULT_NAME, DEFAULT_PORT, DOMAIN, PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    name = entry.data.get(CONF_NAME, DEFAULT_NAME)

    client = FroehlingPe1WebClient(async_get_clientsession(hass), host, port, name)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {DATA_CLIENT: client}

    await client.async_validate()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    client.start()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    data = hass.data.get(DOMAIN, {}).get(entry.entry_id)
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if data and unload_ok:
        client: FroehlingPe1WebClient = data[DATA_CLIENT]
        await client.async_stop()
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
