# Sensorbox Integration for Home Assistant

## Overview

The Sensorbox integration allows you to integrate your Sensorbox 1.5 with Home Assistant. This integration provides real-time power consumption data for your home or specific circuits, enabling you to monitor and analyze your energy usage effectively.

## Features

- Real-time power monitoring for up to three phases (L1, L2, L3)
- Hourly power consumption calculation
- Customizable update interval
- Easy integration with Home Assistant's Energy Dashboard
- Calibration option for improved accuracy

## Requirements

- Sensorbox 1.5 connected to your local network

## Installation

### HACS (Recommended)

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. In the HACS panel, go to "Integrations".
3. Click on the three dots in the top right corner and select "Custom repositories".
4. Add the URL of this repository: `git@github.com:kasperiio/sensorbox-15-custom-component`.
5. Select "Integration" as the category.
6. Click "ADD".
7. Close the custom repositories window.
8. Click the "+ EXPLORE & DOWNLOAD REPOSITORIES" button.
9. Search for "Sensorbox 1.5" and select it.
10. Click "Download" in the bottom right corner.
11. Restart Home Assistant.

### Manual Installation

1. Download the `sensorbox15` folder from this repository.
2. Copy the folder to your `config/custom_components` directory.
3. Restart Home Assistant.

## Configuration

1. In Home Assistant, go to Configuration > Integrations.
2. Click the "+ ADD INTEGRATION" button.
3. Search for "Sensorbox" and select it.
4. Follow the configuration steps:
   - Enter the IP address of your Sensorbox.
   - Enter the Modbus port (default is 502).
   - Set the calibration value (default is 1.0, adjust if needed for accuracy).
   - Configure the update interval (optional).

## Usage

After setting up the integration, you'll have access to the following sensors:

- `sensor.sensorbox15_l1_power`: Power consumption on L1 phase
- `sensor.sensorbox15_l2_power`: Power consumption on L2 phase
- `sensor.sensorbox15_l3_power`: Power consumption on L3 phase
- `sensor.sensorbox15_total_power`: Total power consumption across all phases
- `sensor.sensorbox15_hourly_consumption`: Hourly consumption calculation

You can use these sensors in your automations, scripts, or add them to your Energy Dashboard for comprehensive energy monitoring.

### Adding to Energy Dashboard

To add the Sensorbox data to your Energy Dashboard:

1. Go to Configuration > Energy.
2. In the "Electricity grid" section, click "Add consumption".
3. Select the `sensor.sensorbox15_hourly_consumption` entity.
4. Click "Save".

Now your Sensorbox data will be included in your Energy Dashboard visualizations.

## Troubleshooting

If you encounter any issues:

1. Ensure your Sensorbox is connected to your network.
2. Check that the IP address and port are correct in the configuration.
3. Verify that your Home Assistant instance can reach the Sensorbox on your network.
4. Check the Home Assistant logs for any error messages related to the Sensorbox integration.
5. If you're experiencing accuracy issues, try adjusting the calibration value in the integration settings.

## Contributing

Contributions to improve the Sensorbox integration are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

This integration is released under the MIT License.

## Disclaimer

This integration is not officially associated with or endorsed by the Sensorbox manufacturer SmartEVSE. Use at your own risk.