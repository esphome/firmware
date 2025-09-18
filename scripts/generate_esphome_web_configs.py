#!/usr/bin/env python3
"""
Script to generate ESPHome Web configuration files from templates.

This script generates both regular and factory configurations for different
ESP32 variants, ESP8266, and Raspberry Pi Pico W platforms.

Requires Python 3.13+ for modern typing features (TypedDict, Literal, etc.)

Usage:
    python3 scripts/generate_esphome_web_configs.py
"""

import sys
from pathlib import Path
from typing import Literal, NotRequired, TypedDict

# Check Python version
if sys.version_info < (3, 13):
    print("Error: This script requires Python 3.13 or higher")
    print(f"Current version: {sys.version}")
    sys.exit(1)

# Configuration constants
MIN_VERSION: str = "2025.9.0"

# Type definitions for platform configuration
PlatformKey = Literal["esp32", "esp8266", "rp2040"]


class FrameworkConfig(TypedDict):
    type: Literal["arduino", "esp-idf"]


class BoardConfig(TypedDict, total=False):
    # ESP32 platforms use variant
    variant: Literal["esp32", "esp32c3", "esp32c6", "esp32s2", "esp32s3"]
    framework: FrameworkConfig
    # ESP8266 and RP2040 use board
    board: Literal["esp01_1m", "rpipicow"]


class PlatformConfig(TypedDict):
    board_config: BoardConfig
    has_bluetooth: bool
    has_captive_portal: bool
    platform_key: NotRequired[PlatformKey]


# Platform configurations
PLATFORMS: dict[str, PlatformConfig] = {
    "esp32": {
        "board_config": {"variant": "esp32", "framework": {"type": "esp-idf"}},
        "has_bluetooth": True,
        "has_captive_portal": True,
    },
    "esp32c3": {
        "board_config": {"variant": "esp32c3", "framework": {"type": "esp-idf"}},
        "has_bluetooth": True,
        "has_captive_portal": True,
    },
    "esp32c6": {
        "board_config": {"variant": "esp32c6", "framework": {"type": "esp-idf"}},
        "has_bluetooth": True,
        "has_captive_portal": True,
    },
    "esp32s2": {
        "board_config": {"variant": "esp32s2", "framework": {"type": "esp-idf"}},
        "has_bluetooth": False,
        "has_captive_portal": True,
    },
    "esp32s3": {
        "board_config": {"variant": "esp32s3", "framework": {"type": "esp-idf"}},
        "has_bluetooth": True,
        "has_captive_portal": True,
    },
    "esp8266": {
        "board_config": {"board": "esp01_1m"},
        "has_bluetooth": False,
        "has_captive_portal": True,
        "platform_key": "esp8266",
    },
    "pico-w": {
        "board_config": {"board": "rpipicow"},
        "has_bluetooth": False,
        "has_captive_portal": False,
        "platform_key": "rp2040",
    },
}


def create_base_config(platform_name: str, platform_config: PlatformConfig) -> str:
    """Create the base configuration for a platform."""
    # Build platform section
    platform_key: str = platform_config.get("platform_key", "esp32")
    platform_section: str = f"{platform_key}:\n"

    board_config: BoardConfig = platform_config["board_config"]
    for key, value in board_config.items():
        if isinstance(value, dict):
            platform_section += f"  {key}:\n"
            for sub_key, sub_value in value.items():
                platform_section += f"    {sub_key}: {sub_value}\n"
        else:
            platform_section += f"  {key}: {value}\n"

    # Combine all sections
    config: str = f"""esphome:
  name: esphome-web
  friendly_name: ESPHome Web
  min_version: {MIN_VERSION}
  name_add_mac_suffix: true

{platform_section}
# Enable logging
logger:

# Enable Home Assistant API
api:

# Allow Over-The-Air updates
ota:
  - platform: esphome

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
"""

    return config


def create_factory_config(platform_name: str, platform_config: PlatformConfig) -> str:
    """Create the factory configuration for a platform."""
    # Build platform section
    platform_key: str = platform_config.get("platform_key", "esp32")
    platform_section: str = f"{platform_key}:\n"

    board_config: BoardConfig = platform_config["board_config"]
    for key, value in board_config.items():
        if isinstance(value, dict):
            platform_section += f"  {key}:\n"
            for sub_key, sub_value in value.items():
                platform_section += f"    {sub_key}: {sub_value}\n"
        else:
            platform_section += f"  {key}: {value}\n"

    # Build the factory config with full configuration
    config: str = f"""esphome:
  name: esphome-web
  friendly_name: ESPHome Web
  min_version: {MIN_VERSION}
  name_add_mac_suffix: true
  project:
    name: esphome.web
    version: dev

{platform_section}
# Enable logging
logger:

# Enable Home Assistant API
api:

# Allow Over-The-Air updates
ota:
  - platform: esphome

# Allow provisioning Wi-Fi via serial
improv_serial:

wifi:
  # Set up a wifi access point
  ap: {{}}"""

    # Add captive portal for platforms that support it
    has_captive_portal: bool = platform_config.get("has_captive_portal", True)
    if has_captive_portal:
        config += """

# In combination with the `ap` this allows the user
# to provision wifi credentials to the device via WiFi AP.
captive_portal:"""

    config += f"""

# Allows taking control of the device in the ESPHome Builder/Dashboard
dashboard_import:
  package_import_url: github://esphome/firmware/esphome-web/{platform_name}.yaml@main
  import_full_config: true"""

    # Add Bluetooth support for platforms that support it
    has_bluetooth: bool = platform_config["has_bluetooth"]
    if has_bluetooth:
        config += """

# Sets up Bluetooth LE (Only on ESP32) to allow the user
# to provision wifi credentials to the device.
esp32_improv:
  authorizer: none"""

    config += "\n"
    return config


def write_yaml_file(filepath: str | Path, config: str) -> None:
    """Write configuration to YAML file with proper formatting."""
    # Ensure directory exists using pathlib
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w") as f:
        f.write(config)

    print(f"Generated: {filepath}")


def main() -> None:
    """Generate all ESPHome Web configuration files."""
    script_dir: Path = Path(__file__).parent
    repo_root: Path = script_dir.parent
    esphome_web_dir: Path = repo_root / "esphome-web"

    print("Generating ESPHome Web configuration files...")
    print(f"Output directory: {esphome_web_dir}")

    for platform_name, platform_config in PLATFORMS.items():
        # Generate base configuration
        base_config: str = create_base_config(platform_name, platform_config)
        base_filepath: Path = esphome_web_dir / f"{platform_name}.yaml"
        write_yaml_file(base_filepath, base_config)

        # Generate factory configuration
        factory_config: str = create_factory_config(platform_name, platform_config)
        factory_filepath: Path = esphome_web_dir / f"{platform_name}.factory.yaml"
        write_yaml_file(factory_filepath, factory_config)

    print("\nGeneration complete!")


if __name__ == "__main__":
    main()
