# Scripts

This directory contains utility scripts for maintaining the ESPHome firmware configurations.

## generate_esphome_web_configs.py

Generates all ESPHome Web configuration files from templates based on platform-specific settings.

### Features

- **Platform Support**: Generates configs for ESP32 variants, ESP8266, and Raspberry Pi Pico W
- **Bluetooth Awareness**: Automatically excludes Bluetooth features for platforms that don't support it:
  - ESP8266
  - ESP32-S2  
  - Raspberry Pi Pico W
- **Template-based**: Uses consistent templates for base and factory configurations
- **Automatic File Generation**: Creates both regular and factory YAML files for each platform

### Platform Configurations

| Platform | Variant/Board | Framework | Bluetooth | Min Version |
| -------- | ------------- | --------- | --------- | ----------- |
| ESP32    | esp32         | ESP-IDF   | ✅         | 2025.9.0    |
| ESP32-C3 | esp32c3       | ESP-IDF   | ✅         | 2025.9.0    |
| ESP32-C6 | esp32c6       | ESP-IDF   | ✅         | 2025.9.0    |
| ESP32-S2 | esp32s2       | ESP-IDF   | ❌         | 2025.9.0    |
| ESP32-S3 | esp32s3       | ESP-IDF   | ✅         | 2025.9.0    |
| ESP8266  | esp01_1m      | Arduino   | ❌         | 2025.9.0    |
| Pico W   | rpipicow      | Arduino   | ❌         | 2025.9.0    |

### Usage

```bash
# Run from the repository root
python3 scripts/generate_esphome_web_configs.py

# Or run directly (script is executable)
./scripts/generate_esphome_web_configs.py
```

### Generated Files

The script generates files in the `esphome-web/` directory:

**Base configurations** (for taking control with secrets):
- `esp32.yaml`
- `esp32c3.yaml` 
- `esp32c6.yaml`
- `esp32s2.yaml`
- `esp32s3.yaml`
- `esp8266.yaml`
- `pico-w.yaml`

**Factory configurations** (for distribution with provisioning):
- `esp32.factory.yaml`
- `esp32c3.factory.yaml`
- `esp32c6.factory.yaml` 
- `esp32s2.factory.yaml`
- `esp32s3.factory.yaml`
- `esp8266.factory.yaml`
- `pico-w.factory.yaml`

### Configuration Differences

#### Base vs Factory Configurations

**Base configurations** include:
- WiFi credentials from secrets
- Basic ESPHome, API, OTA, and logging components

**Factory configurations** include:
- WiFi AP mode for provisioning
- Captive portal for WiFi setup
- Serial provisioning (`improv_serial`)
- Dashboard import URLs
- Bluetooth provisioning (`esp32_improv`) for supported platforms
- Project metadata

#### Bluetooth Support

Platforms **with** Bluetooth support get:
- `esp32_improv` component for Bluetooth provisioning

Platforms **without** Bluetooth support:
- ESP8266: Limited hardware capabilities
- ESP32-S2: No Bluetooth radio
- Raspberry Pi Pico W: No Bluetooth support in ESPHome

### Customization

To modify the generated configurations:

1. Edit the `PLATFORMS` dictionary in the script
2. Modify the `create_base_config()` or `create_factory_config()` functions
3. Run the script to regenerate all files

### Dependencies

- Python 3.13+
- No external dependencies (uses only standard library)
