"""Sensorbox 1.5 integration."""

import asyncio
import logging
import struct

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ConnectionException

from homeassistant.exceptions import ConfigEntryNotReady

_LOGGER = logging.getLogger(__name__)

MAX_RETRIES = 3
RETRY_DELAY = 5


class Sensorbox:
    """Sensorbox 1.5 integration class."""

    def __init__(self, host: str, port: int, calibration: float):
        """Initialize the Sensorbox 1.5 integration."""
        self.host = host
        self.port = port
        self.calibration = calibration
        self.client = None
        self.data = {}

    async def async_setup(self):
        """Set up the Sensorbox 1.5 client."""
        for attempt in range(MAX_RETRIES):
            try:
                self.client = AsyncModbusTcpClient(self.host, port=self.port)
                if await self.client.connect():
                    _LOGGER.debug(
                        f"Successfully connected to Sensorbox 1.5 at {self.host}:{self.port}"
                    )
                    return
                else:
                    _LOGGER.warning(
                        f"Failed to connect to Sensorbox 1.5 at {self.host}:{self.port}, attempt {attempt + 1}/{MAX_RETRIES}"
                    )
            except ConnectionException as exc:
                _LOGGER.warning(
                    f"Connection error to Sensorbox 1.5: {exc}, attempt {attempt + 1}/{MAX_RETRIES}"
                )
            except Exception as exc:
                _LOGGER.error(
                    f"Unexpected error connecting to Sensorbox 1.5: {exc}, attempt {attempt + 1}/{MAX_RETRIES}"
                )

            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(RETRY_DELAY)

        raise ConfigEntryNotReady(
            f"Failed to connect to Sensorbox 1.5 at {self.host}:{self.port} after {MAX_RETRIES} attempts"
        )

    async def async_update_data(self):
        """Update data via library."""
        if not self.client or not self.client.connected:
            await self.async_setup()

        try:
            power_data = await self.read_power_module()

            self.data = power_data
            _LOGGER.debug("Updated Sensorbox 1.5 data: %s", self.data)
            return self.data
        except ConnectionException as error:
            _LOGGER.error("Error connecting to Sensorbox 1.5: %s", error)
            raise

    async def read_power_module(self):
        """Read power module data."""
        response = await self.client.read_input_registers(address=0, count=20, slave=10)
        if not response.isError():
            return self.parse_power_module(response.registers)
        _LOGGER.error("Modbus error reading power module: %s", response)
        return {}

    def parse_power_module(self, registers):
        """Parse power module data."""
        l1 = self.read_float(registers, 0x10) * 230 * self.calibration
        l2 = self.read_float(registers, 0x12) * 230 * self.calibration
        l3 = self.read_float(registers, 0x0E) * 230 * self.calibration
        full = l1 + l2 + l3
        return {
            "l1_power": l1,
            "l2_power": l2,
            "l3_power": l3,
            "total_power": full,
        }

    @staticmethod
    def read_float(registers, index):
        """Read float from registers."""
        return struct.unpack(
            ">f", struct.pack(">HH", registers[index], registers[index + 1])
        )[0]

    async def async_close(self):
        """Close the Modbus client."""
        if self.client:
            self.client.close()
