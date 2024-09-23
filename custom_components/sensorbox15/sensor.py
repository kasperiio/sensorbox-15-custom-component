"""Platform for Sensorbox 1.5 sensor integration."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, POWER_SENSORS


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Sensorbox 1.5 sensors."""
    power_coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    energy_coordinator = hass.data[DOMAIN][config_entry.entry_id]["energy_coordinator"]
    entities = []

    for sensor_id, details in POWER_SENSORS.items():
        cls = SensorboxPowerSensor
        coordinator = power_coordinator
        if sensor_id == "consumption":
            cls = SensorboxConsumptionSensor
            coordinator = energy_coordinator
        entities.append(cls(coordinator, config_entry, sensor_id, details))

    async_add_entities(entities, True)


class SensorboxSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensorbox 1.5 Sensor."""

    def __init__(self, coordinator, config_entry, sensor_id, details):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._attr_name = f"{DOMAIN} {details["name"]}"
        self._attr_native_unit_of_measurement = details["unit"]
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_id}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return round(self.coordinator.data.get(self._sensor_id), 2)

    @property
    def device_info(self):
        """Return device information about this Sensorbox 1.5 device."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.config_entry.entry_id)},
            "name": "Sensorbox 1.5",
            "manufacturer": "SmartEVSE",
            "model": "Sensorbox 1.5",
        }


class SensorboxPowerSensor(SensorboxSensor):
    """Representation of a Sensorbox 1.5 power sensor."""

    def __init__(self, coordinator, config_entry, sensor_id, details):
        """Initialize the sensor."""
        super().__init__(coordinator, config_entry, sensor_id, details)
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT


class SensorboxConsumptionSensor(SensorboxSensor):
    """Representation of a Sensorbox 1.5 consumption sensor."""

    def __init__(self, coordinator, config_entry, sensor_id, details):
        """Initialize the energy usage sensor."""
        super().__init__(coordinator, config_entry, sensor_id, details)
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
