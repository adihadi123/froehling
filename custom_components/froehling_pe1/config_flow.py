from __future__ import annotations

import voluptuous as vol
from aiohttp import ClientError
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .client import FroehlingPe1WebClient
from .const import CONF_HOST, CONF_NAME, CONF_PORT, DEFAULT_NAME, DEFAULT_PORT, DOMAIN


class FroehlingPe1ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Fröling PE1 Web."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input.get(CONF_PORT, DEFAULT_PORT)
            name = user_input.get(CONF_NAME, DEFAULT_NAME)

            await self.async_set_unique_id(f"{host}:{port}")
            self._abort_if_unique_id_configured(updates={CONF_HOST: host, CONF_PORT: port})

            client = FroehlingPe1WebClient(
                async_get_clientsession(self.hass), host, port, name
            )
            try:
                await client.async_validate()
            except (ClientError, TimeoutError, OSError):
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=name, data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default="192.168.178.192"): str,
                vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
