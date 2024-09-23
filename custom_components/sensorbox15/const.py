"""Constants for the Sensorbox 1.5 integration."""

DOMAIN = "sensorbox15"

DEFAULT_MODBUS_PORT = 26
DEFAULT_POLL_INTERVAL = 3
DEFAULT_CALIBRATION = 1.00

POWER_SENSORS = {
    "l1_power": {"name": "L1 Power", "unit": "W"},
    "l2_power": {"name": "L2 Power", "unit": "W"},
    "l3_power": {"name": "L3 Power", "unit": "W"},
    "total_power": {"name": "Total Power", "unit": "W"},
    "consumption": {"name": "Hourly Consumption", "unit": "Wh"},
}
