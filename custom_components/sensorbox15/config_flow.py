"""Config flow for Sensorbox 1.5 integration."""

from __future__ import annotations

import asyncio
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    DEFAULT_CALIBRATION,
    DEFAULT_MODBUS_PORT,
    DEFAULT_POLL_INTERVAL,
    DOMAIN,
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default=DEFAULT_MODBUS_PORT): int,
        vol.Optional("poll_interval", default=DEFAULT_POLL_INTERVAL): int,
        vol.Optional("calibration", default=DEFAULT_CALIBRATION): vol.Coerce(float),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    from pymodbus.client import AsyncModbusTcpClient
    from pymodbus.exceptions import ConnectionException, ModbusException

    host = data[CONF_HOST]
    port = data[CONF_PORT]

    client = AsyncModbusTcpClient(host, port=port)
    try:
        await client.connect()
        if not client.connected:
            raise CannotConnect("Failed to connect to the Modbus server")

        # Try to read registers to confirm communication
        result = await client.read_input_registers(address=0, count=20, slave=10)
        if result.isError():
            raise CannotConnect(f"Error reading registers: {result}")

        # If we get here, the connection is successful and we can read the registers
        return {"title": f"Sensorbox 1.5 ({host})"}
    except ConnectionException as conn_err:
        raise CannotConnect(f"Connection error: {conn_err}") from conn_err
    except ModbusException as modbus_err:
        raise CannotConnect(f"Modbus error: {modbus_err}") from modbus_err
    except asyncio.TimeoutError:
        raise CannotConnect("Connection timed out") from None
    except Exception as err:
        raise CannotConnect(f"Unexpected error: {err}") from err
    finally:
        client.close()


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sensorbox 1.5."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidHost:
                errors["host"] = "invalid_host"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Sensorbox 1.5 integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = {
            vol.Optional(
                "poll_interval",
                default=self.config_entry.options.get(
                    "poll_interval", DEFAULT_POLL_INTERVAL
                ),
            ): int,
            vol.Optional(
                "calibration",
                default=self.config_entry.options.get(
                    "calibration", DEFAULT_CALIBRATION
                ),
            ): float,
        }

        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidHost(HomeAssistantError):
    """Error to indicate there is an invalid hostname."""
