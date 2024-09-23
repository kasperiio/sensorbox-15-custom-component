"""DataUpdateCoordinator for Sensorbox 1.5."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .energy import calculate_energy_usage
from .sensorbox import Sensorbox

_LOGGER = logging.getLogger(__name__)


class SensorboxCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Sensorbox 1.5 data."""

    def __init__(
        self, hass: HomeAssistant, sensorbox: Sensorbox, poll_interval: int
    ) -> None:
        """Initialize global Sensorbox 1.5 data updater."""
        self.sensorbox = sensorbox
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=poll_interval),
        )

    async def _async_update_data(self):
        """Fetch data from Sensorbox 1.5."""
        try:
            return await self.sensorbox.async_update_data()
        except ConfigEntryAuthFailed as err:
            raise ConfigEntryAuthFailed from err
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Sensorbox 1.5: {err}")


class SensorboxEnergyCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Sensorbox 1.5 energy data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize Sensorbox 1.5 energy data updater."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_energy",
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self):
        """Calculate energy usage for the last 24 hours."""
        total_power_entity_id = f"sensor.{DOMAIN}_total_power"
        end_time = dt_util.utcnow()
        start_time = end_time.replace(minute=0, second=0, microsecond=0)

        try:
            energy_kwh = await calculate_energy_usage(
                self.hass, total_power_entity_id, start_time, end_time
            )
            return {"consumption": energy_kwh}
        except AttributeError:
            raise HomeAssistantError("Recorder component not yet initialized")
