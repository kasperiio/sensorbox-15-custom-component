"""Energy calculation helper for Sensorbox 1.5 Powermodule."""

import logging

from homeassistant.components import recorder
from homeassistant.exceptions import HomeAssistantError
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)


async def calculate_energy_usage(hass, entity_id, start_time, end_time):
    """Calculate energy usage based on power readings."""
    try:
        _LOGGER.debug(
            f"Fetching history for {entity_id} from {start_time} to {end_time}"
        )
        history = await recorder.get_instance(hass).async_add_executor_job(
            recorder.history.get_significant_states,
            hass,
            start_time,
            end_time,
            [entity_id],
        )
    except AttributeError:
        _LOGGER.error("Recorder component not yet initialized")
        raise HomeAssistantError("Recorder component not yet initialized")

    if not history or entity_id not in history:
        _LOGGER.warning(f"No history found for {entity_id}")
        return 0

    states = history[entity_id]
    energy_kwh = 0
    last_state = None
    last_time = None

    for state in states:
        if state.state in ("unknown", "unavailable"):
            continue

        try:
            current_power = float(state.state)
        except ValueError:
            continue

        current_time = dt_util.as_utc(state.last_updated)

        if last_state is not None and last_time is not None:
            time_diff = (
                current_time - last_time
            ).total_seconds() / 3600  # Convert to hours
            avg_power = (current_power + float(last_state.state)) / 2
            energy_kwh += (avg_power * time_diff) / 1000  # Convert to kWh

        last_state = state
        last_time = current_time

    return energy_kwh
