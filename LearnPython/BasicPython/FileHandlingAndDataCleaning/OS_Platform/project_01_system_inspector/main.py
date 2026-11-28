import json
import os
from datetime import datetime, timezone

from system_info import collect_system_info
from environment_info import collect_selected_environment


# Resolve the project folder from this Python file, not from the terminal CWD.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "settings.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def load_settings():
    """Load project settings from the config folder."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


def main():
    # Create output folder if it does not already exist.
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    settings = load_settings()
    report = {
        "report_created_at_utc": datetime.now(timezone.utc).isoformat(),
        "system": collect_system_info(),
    }

    if settings.get("include_selected_environment", False):
        keys = settings.get("environment_keys", [])
        report["selected_environment"] = collect_selected_environment(keys)

    output_filename = settings.get("report_filename", "system_report.json")
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(report, output_file, indent=4)

    print("System inspection completed.")
    print("Operating system:", report["system"]["os_name"])
    print("Python version:", report["system"]["python_version"])
    print("Report saved to:", output_path)


if __name__ == "__main__":
    main()
